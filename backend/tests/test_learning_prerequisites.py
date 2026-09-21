"""
Prerequisite logic — pure functions, no database.

Two rules live in app/services/learning/prerequisites.py: a directed graph for
course prerequisites (must be acyclic) and an "at least k of these" threshold
for field prerequisites (Multimodal: any one of NLP / Vision / Speech).
"""
import pytest

from app.services.learning.prerequisites import (
    PrerequisiteCycleError, evaluate_threshold, find_cycle, topological_order,
    transitive_prerequisites,
)


# ─── find_cycle ─────────────────────────────────────────────────────────────

def test_acyclic_graph_has_no_cycle():
    assert find_cycle({"c": ["b"], "b": ["a"], "a": []}) is None


def test_empty_graph_has_no_cycle():
    assert find_cycle({}) is None


def test_diamond_is_not_mistaken_for_a_cycle():
    # d needs b and c, both need a: a is reachable by two routes, which is
    # legal and is exactly what a depth-first search with one visited-set
    # gets wrong.
    assert find_cycle({"d": ["b", "c"], "b": ["a"], "c": ["a"], "a": []}) is None


def test_finds_a_simple_cycle_as_a_closed_path():
    cycle = find_cycle({"a": ["b"], "b": ["c"], "c": ["a"]})
    assert cycle is not None
    assert cycle[0] == cycle[-1]
    assert set(cycle) == {"a", "b", "c"}


def test_self_loop_is_a_cycle():
    assert find_cycle({"a": ["a"]}) == ["a", "a"]


def test_cycle_reachable_only_through_a_leaf_target():
    # "z" appears only as a target; the cycle is elsewhere in the graph.
    cycle = find_cycle({"x": ["z"], "a": ["b"], "b": ["a"]})
    assert cycle is not None and set(cycle) == {"a", "b"}


def test_deep_chain_does_not_hit_the_recursion_limit():
    edges = {i: [i - 1] for i in range(1, 5000)}
    edges[0] = []
    assert find_cycle(edges) is None


# ─── topological_order ──────────────────────────────────────────────────────

def test_prerequisites_come_first():
    assert topological_order(["c", "b", "a"], {"c": ["b"], "b": ["a"]}) == ["a", "b", "c"]


def test_order_is_stable_when_nothing_forces_a_move():
    assert topological_order(["x", "y", "z"], {}) == ["x", "y", "z"]


def test_only_the_forced_node_moves():
    # y needs z; x is unrelated and stays first.
    assert topological_order(["x", "y", "z"], {"y": ["z"]}) == ["x", "z", "y"]


def test_prerequisites_outside_the_set_are_ignored():
    # "ghost" is not being ordered here, so it cannot hold "a" back.
    assert topological_order(["a", "b"], {"a": ["ghost"]}) == ["a", "b"]


def test_cycle_raises_instead_of_returning_a_partial_order():
    with pytest.raises(PrerequisiteCycleError) as info:
        topological_order(["a", "b"], {"a": ["b"], "b": ["a"]})
    assert set(info.value.cycle) >= {"a", "b"}


# ─── transitive_prerequisites ───────────────────────────────────────────────

def test_transitive_prerequisites_nearest_first_without_repeats():
    edges = {"d": ["c", "b"], "c": ["a"], "b": ["a"]}
    assert transitive_prerequisites("d", edges) == ["c", "b", "a"]


def test_transitive_prerequisites_terminates_on_a_cycle():
    edges = {"a": ["b"], "b": ["a"]}
    assert set(transitive_prerequisites("a", edges)) == {"b"}


# ─── evaluate_threshold ─────────────────────────────────────────────────────

MODALITIES = ["nlp", "computer-vision", "speech"]


def test_any_one_of_three_meets_the_requirement_but_not_the_recommendation():
    r = evaluate_threshold(MODALITIES, ["nlp"], min_required=1, recommended=2)
    assert r.met and not r.recommended_met
    assert r.satisfied == ["nlp"]
    assert r.missing == ["computer-vision", "speech"]
    assert r.shortfall == 0


def test_two_modalities_meet_the_recommendation():
    r = evaluate_threshold(MODALITIES, ["nlp", "speech"], min_required=1, recommended=2)
    assert r.met and r.recommended_met


def test_none_owned_reports_the_shortfall():
    r = evaluate_threshold(MODALITIES, [], min_required=1, recommended=2)
    assert not r.met and not r.recommended_met
    assert r.shortfall == 1


def test_unrelated_fields_do_not_count():
    r = evaluate_threshold(MODALITIES, ["data", "machine-learning"], min_required=1, recommended=1)
    assert not r.met


def test_a_rule_cannot_demand_more_than_exists():
    # "2 of these" over one listed field would be unsatisfiable; it is capped
    # so a data mistake never becomes a wall in front of the learner.
    r = evaluate_threshold(["nlp"], ["nlp"], min_required=2, recommended=3)
    assert r.met and r.recommended_met


def test_no_prerequisites_is_always_met():
    r = evaluate_threshold([], [], min_required=1, recommended=1)
    assert r.met and r.recommended_met and r.shortfall == 0


def test_stricter_rule_is_just_a_different_number():
    r = evaluate_threshold(MODALITIES, ["nlp"], min_required=2, recommended=2)
    assert not r.met and r.shortfall == 1


def test_duplicate_prerequisites_are_counted_once():
    r = evaluate_threshold(["nlp", "nlp", "speech"], ["nlp"], min_required=2, recommended=2)
    assert r.satisfied == ["nlp"] and r.missing == ["speech"]
