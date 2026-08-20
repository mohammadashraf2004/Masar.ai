from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import Optional, List

from app.db.session import get_db
from app.models.user import User
from app.models.community import Post, PostLike, PostComment, UserFollow, PostType
from app.views.community import (
    PostCreate, PostUpdate, PostResponse, PostListResponse,
    CommentCreate, CommentResponse,
    FollowResponse, LeaderboardResponse, LeaderboardEntry, AuthorMini,
)
from app.core.security import get_current_user

router = APIRouter(prefix="/community", tags=["Community"])


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _liked_by(post: Post, user_id: int) -> bool:
    return any(like.user_id == user_id for like in post.likes)


def _post_to_response(post: Post, current_user_id: int) -> PostResponse:
    return PostResponse(
        **{c.name: getattr(post, c.name) for c in post.__table__.columns},
        author=post.author,
        liked_by_me=_liked_by(post, current_user_id),
        comments=post.comments,
    )


# ─── Feed ────────────────────────────────────────────────────────────────────

@router.get("/feed", response_model=PostListResponse)
def get_feed(
    post_type: Optional[PostType] = None,
    tag: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = (
        db.query(Post)
        .options(
            joinedload(Post.author),
            joinedload(Post.likes),
            joinedload(Post.comments).joinedload(PostComment.author),
        )
    )

    if post_type:
        q = q.filter(Post.post_type == post_type)
    if tag:
        q = q.filter(Post.tags.contains([tag]))

    total = q.count()
    posts = (
        q.order_by(desc(Post.is_pinned), desc(Post.created_at))
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return PostListResponse(
        posts=[_post_to_response(p, current_user.id) for p in posts],
        total=total,
        page=page,
        per_page=per_page,
    )


# ─── Create post ─────────────────────────────────────────────────────────────

@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = Post(
        author_id=current_user.id,
        post_type=payload.post_type,
        title=payload.title,
        content=payload.content,
        github_url=payload.github_url,
        image_url=payload.image_url,
        tags=payload.tags,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    # reload with relationships
    post = db.query(Post).options(
        joinedload(Post.author),
        joinedload(Post.likes),
        joinedload(Post.comments),
    ).filter(Post.id == post.id).first()
    return _post_to_response(post, current_user.id)


# ─── Single post ─────────────────────────────────────────────────────────────

@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).options(
        joinedload(Post.author),
        joinedload(Post.likes),
        joinedload(Post.comments).joinedload(PostComment.author),
    ).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return _post_to_response(post, current_user.id)


# ─── Update / delete post ────────────────────────────────────────────────────

@router.patch("/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    payload: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your post")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    post = db.query(Post).options(
        joinedload(Post.author), joinedload(Post.likes),
        joinedload(Post.comments).joinedload(PostComment.author),
    ).filter(Post.id == post_id).first()
    return _post_to_response(post, current_user.id)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your post")
    db.delete(post)
    db.commit()


# ─── Like / unlike ───────────────────────────────────────────────────────────

@router.post("/posts/{post_id}/like", status_code=status.HTTP_200_OK)
def toggle_like(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == current_user.id,
    ).first()

    if existing:
        db.delete(existing)
        post.likes_count = max(0, post.likes_count - 1)
        liked = False
    else:
        db.add(PostLike(post_id=post_id, user_id=current_user.id))
        post.likes_count += 1
        liked = True

    db.commit()
    return {"liked": liked, "likes_count": post.likes_count}


# ─── Comments ────────────────────────────────────────────────────────────────

@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment(
    post_id: int,
    payload: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment = PostComment(
        post_id=post_id,
        author_id=current_user.id,
        content=payload.content,
    )
    db.add(comment)
    post.comments_count += 1
    db.commit()
    db.refresh(comment)
    # reload with author
    comment = db.query(PostComment).options(
        joinedload(PostComment.author)
    ).filter(PostComment.id == comment.id).first()
    return comment


@router.delete("/posts/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    post_id: int,
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comment = db.query(PostComment).filter(
        PostComment.id == comment_id,
        PostComment.post_id == post_id,
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your comment")

    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.comments_count = max(0, post.comments_count - 1)

    db.delete(comment)
    db.commit()


# ─── Follow / unfollow ───────────────────────────────────────────────────────

@router.post("/users/{user_id}/follow", response_model=FollowResponse)
def toggle_follow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(UserFollow).filter(
        UserFollow.follower_id == current_user.id,
        UserFollow.following_id == user_id,
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return FollowResponse(following_id=user_id, is_following=False)
    else:
        db.add(UserFollow(follower_id=current_user.id, following_id=user_id))
        db.commit()
        return FollowResponse(following_id=user_id, is_following=True)


@router.get("/users/{user_id}/posts", response_model=PostListResponse)
def user_posts(
    user_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Post).options(
        joinedload(Post.author),
        joinedload(Post.likes),
        joinedload(Post.comments).joinedload(PostComment.author),
    ).filter(Post.author_id == user_id)

    total = q.count()
    posts = q.order_by(desc(Post.created_at)).offset((page - 1) * per_page).limit(per_page).all()

    return PostListResponse(
        posts=[_post_to_response(p, current_user.id) for p in posts],
        total=total, page=page, per_page=per_page,
    )


# ─── Leaderboard ─────────────────────────────────────────────────────────────

@router.get("/leaderboard", response_model=LeaderboardResponse)
def leaderboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Get top 20 users by posts + likes received
    rows = (
        db.query(
            User,
            func.count(Post.id).label("posts_count"),
            func.coalesce(func.sum(Post.likes_count), 0).label("likes_received"),
        )
        .outerjoin(Post, Post.author_id == User.id)
        .group_by(User.id)
        .order_by(
            desc(func.coalesce(func.sum(Post.likes_count), 0)),
            desc(func.count(Post.id)),
        )
        .limit(20)
        .all()
    )

    entries = [
        LeaderboardEntry(
            rank=i + 1,
            user=AuthorMini(
                id=user.id,
                full_name=user.full_name,
                experience_level=user.experience_level,
                overall_readiness_score=user.overall_readiness_score,
                avatar_url=user.avatar_url,
            ),
            posts_count=posts_count,
            likes_received=likes_received,
            readiness_score=user.overall_readiness_score,
        )
        for i, (user, posts_count, likes_received) in enumerate(rows)
    ]

    return LeaderboardResponse(entries=entries)