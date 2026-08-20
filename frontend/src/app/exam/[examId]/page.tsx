"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { ExamPaymentGate } from "@/components/ui/ExamPaymentGate";
import { AppShell } from "@/components/layout/AppShell";
import { Card, Badge, Spinner, ProgressBar } from "@/components/ui/index";
import { Button } from "@/components/ui/Button";
import {
  Clock, Shield, ChevronRight, ChevronLeft,
  CheckCircle, XCircle, AlertTriangle, Camera,
  Code2, AlignLeft, ToggleLeft, List, GripVertical,
  CheckSquare, Circle, Trophy, RotateCcw, ShieldCheck
} from "lucide-react";

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────
interface Question {
  id: number;
  question_type: "mcq" | "multi" | "true_false" | "code" | "fill_blank" | "ordering" | "short";
  question_text: string;
  points: number;
  order_index: number;
  options?: string[];
  code_template?: string;
  starter_code?: string;
  language?: string;
}

interface ExamData {
  exam_id: number;
  attempt_id: number;
  title: string;
  description: string;
  duration_minutes: number;
  passing_score: number;
  total_points: number;
  questions: Question[];
  started_at: string;
  proctoring_required: boolean;
}

type Answers = Record<number, string | string[]>;

// ─────────────────────────────────────────────────────────────────────────────
// Utilities
// ─────────────────────────────────────────────────────────────────────────────
function fmtTime(sec: number) {
  const m = Math.floor(sec / 60).toString().padStart(2, "0");
  const s = (sec % 60).toString().padStart(2, "0");
  return `${m}:${s}`;
}

const TYPE_META: Record<string, { label: string; icon: any; variant: string }> = {
  mcq:        { label: "Single choice",   icon: Circle,      variant: "sky" },
  multi:      { label: "Multi select",    icon: CheckSquare, variant: "emerald" },
  true_false: { label: "True / False",    icon: ToggleLeft,  variant: "amber" },
  code:       { label: "Code",            icon: Code2,       variant: "rose" },
  fill_blank: { label: "Fill in blank",   icon: AlignLeft,   variant: "amber" },
  ordering:   { label: "Ordering",        icon: List,        variant: "sky" },
  short:      { label: "Short answer",    icon: AlignLeft,   variant: "ghost" },
};

// ─────────────────────────────────────────────────────────────────────────────
// Question type components
// ─────────────────────────────────────────────────────────────────────────────

function MCQ({ q, value, onChange }: { q: Question; value: string; onChange: (v: string) => void }) {
  return (
    <div className="space-y-2">
      {(q.options ?? []).map((opt) => (
        <button
          key={opt}
          onClick={() => onChange(opt)}
          className={`w-full text-left flex items-center gap-3 px-4 py-3 rounded-lg border text-sm transition-all duration-150 ${
            value === opt
              ? "bg-amber/10 border-amber/40 text-amber"
              : "bg-surface border-border text-soft hover:border-amber/20 hover:text-bright"
          }`}
        >
          <span className={`w-4 h-4 rounded-full border-2 flex-shrink-0 flex items-center justify-center ${
            value === opt ? "border-amber" : "border-muted"
          }`}>
            {value === opt && <span className="w-2 h-2 rounded-full bg-amber" />}
          </span>
          {opt}
        </button>
      ))}
    </div>
  );
}

function MultiChoice({ q, value, onChange }: { q: Question; value: string[]; onChange: (v: string[]) => void }) {
  const toggle = (opt: string) => {
    const cur = value ?? [];
    onChange(cur.includes(opt) ? cur.filter((x) => x !== opt) : [...cur, opt]);
  };
  return (
    <div className="space-y-2">
      {(q.options ?? []).map((opt) => {
        const selected = (value ?? []).includes(opt);
        return (
          <button
            key={opt}
            onClick={() => toggle(opt)}
            className={`w-full text-left flex items-center gap-3 px-4 py-3 rounded-lg border text-sm transition-all duration-150 ${
              selected
                ? "bg-emerald/10 border-emerald/40 text-emerald"
                : "bg-surface border-border text-soft hover:border-emerald/20 hover:text-bright"
            }`}
          >
            <span className={`w-4 h-4 rounded border-2 flex-shrink-0 flex items-center justify-center ${
              selected ? "border-emerald bg-emerald/20" : "border-muted"
            }`}>
              {selected && <CheckCircle size={10} className="text-emerald" />}
            </span>
            {opt}
          </button>
        );
      })}
      <p className="text-xs text-ghost mt-2">Select all that apply</p>
    </div>
  );
}

function TrueFalse({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  return (
    <div className="flex gap-4">
      {["True", "False"].map((v) => (
        <button
          key={v}
          onClick={() => onChange(v)}
          className={`flex-1 py-6 rounded-lg border-2 text-lg font-semibold font-display transition-all duration-150 ${
            value === v
              ? v === "True"
                ? "bg-emerald/10 border-emerald text-emerald"
                : "bg-rose/10 border-rose text-rose"
              : "bg-surface border-border text-dim hover:border-amber/30 hover:text-bright"
          }`}
        >
          {v === "True" ? "✓ True" : "✗ False"}
        </button>
      ))}
    </div>
  );
}

function CodeEditor({ q, value, onChange }: { q: Question; value: string; onChange: (v: string) => void }) {
  const init = value || q.starter_code || "";
  return (
    <div className="rounded-lg border border-border overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 bg-ink border-b border-border">
        <div className="flex items-center gap-2">
          <Code2 size={13} className="text-ghost" />
          <span className="text-xs font-mono text-ghost">{q.language ?? "python"}</span>
        </div>
        <div className="flex gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-rose/40" />
          <span className="w-2.5 h-2.5 rounded-full bg-amber/40" />
          <span className="w-2.5 h-2.5 rounded-full bg-emerald/40" />
        </div>
      </div>
      <textarea
        className="w-full min-h-[280px] bg-void text-sky-300 font-mono text-sm p-4 outline-none resize-y leading-relaxed"
        value={value || init}
        onChange={(e) => onChange(e.target.value)}
        spellCheck={false}
        autoComplete="off"
        style={{ fontFamily: "var(--font-jetbrains), monospace" }}
      />
    </div>
  );
}

function FillBlank({ q, value, onChange }: { q: Question; value: string[]; onChange: (v: string[]) => void }) {
  const template = q.code_template ?? "";
  const blanks = (template.match(/___BLANK_\d+___/g) ?? []).length;
  const vals: string[] = Array.isArray(value) ? value : Array(blanks).fill("");

  const setBlank = (i: number, v: string) => {
    const next = [...vals];
    next[i] = v;
    onChange(next);
  };

  const parts = template.split(/(___BLANK_\d+___)/g);
  return (
    <div className="rounded-lg border border-border overflow-hidden">
      <div className="flex items-center gap-2 px-4 py-2 bg-ink border-b border-border">
        <AlignLeft size={13} className="text-ghost" />
        <span className="text-xs font-mono text-ghost">Fill in the blanks</span>
      </div>
      <pre
        className="p-4 bg-void font-mono text-sm leading-relaxed text-sky-300 overflow-x-auto whitespace-pre-wrap"
        style={{ fontFamily: "var(--font-jetbrains), monospace" }}
      >
        {parts.map((part, i) => {
          const match = part.match(/___BLANK_(\d+)___/);
          if (match) {
            const idx = parseInt(match[1]) - 1;
            return (
              <input
                key={i}
                value={vals[idx] ?? ""}
                onChange={(e) => setBlank(idx, e.target.value)}
                placeholder={`···`}
                className="inline-block bg-amber/10 border border-amber/40 rounded text-amber text-sm font-mono px-2 py-0.5 outline-none focus:border-amber mx-1"
                style={{ width: Math.max(80, (vals[idx]?.length ?? 6) * 9 + 24), fontFamily: "var(--font-jetbrains), monospace" }}
              />
            );
          }
          return <span key={i}>{part}</span>;
        })}
      </pre>
    </div>
  );
}

function Ordering({ q, value, onChange }: { q: Question; value: string[]; onChange: (v: string[]) => void }) {
  const init = Array.isArray(value) && value.length > 0 ? value : [...(q.options ?? [])];
  const [items, setItems] = useState<string[]>(init);
  const dragIdx = useRef<number | null>(null);

  useEffect(() => {
    if (!value || value.length === 0) onChange(items);
  }, []); // eslint-disable-line

  const move = (from: number, to: number) => {
    const next = [...items];
    const [moved] = next.splice(from, 1);
    next.splice(to, 0, moved);
    setItems(next);
    onChange(next);
  };

  return (
    <div className="space-y-2">
      {items.map((item, i) => (
        <div
          key={item}
          draggable
          onDragStart={() => { dragIdx.current = i; }}
          onDragOver={(e) => e.preventDefault()}
          onDrop={() => {
            if (dragIdx.current !== null && dragIdx.current !== i) move(dragIdx.current, i);
            dragIdx.current = null;
          }}
          className="flex items-center gap-3 px-4 py-3 bg-surface border border-border rounded-lg cursor-grab active:cursor-grabbing hover:border-amber/20 transition-colors"
        >
          <span className="w-6 h-6 rounded bg-amber/10 border border-amber/20 flex items-center justify-center text-xs font-mono text-amber flex-shrink-0">
            {i + 1}
          </span>
          <GripVertical size={14} className="text-ghost flex-shrink-0" />
          <span className="text-sm text-soft">{item}</span>
        </div>
      ))}
      <p className="text-xs text-ghost mt-2">↕ Drag to reorder</p>
    </div>
  );
}

function ShortAnswer({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  return (
    <textarea
      className="w-full bg-surface border border-border rounded-lg text-sm text-soft p-4 outline-none focus:border-amber/40 resize-none leading-relaxed transition-colors placeholder:text-ghost"
      value={value ?? ""}
      onChange={(e) => onChange(e.target.value)}
      placeholder="Write your answer here (2–4 sentences recommended)…"
      rows={6}
      style={{ fontFamily: "var(--font-dm-sans), sans-serif" }}
    />
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Main Page
// ─────────────────────────────────────────────────────────────────────────────
export default function ExamPage() {
  const params = useParams();
  const router = useRouter();
  const examId = params?.examId as string;

  const [phase, setPhase] = useState<"loading" | "setup" | "active" | "submitted" | "error">("loading");
  const [exam, setExam] = useState<ExamData | null>(null);
  const [answers, setAnswers] = useState<Answers>({});
  const [current, setCurrent] = useState(0);
  const [timeLeft, setTimeLeft] = useState(0);
  const [violations, setViolations] = useState(0);
  const [violationMsg, setViolationMsg] = useState("");
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [webcamOk, setWebcamOk] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [showPaymentGate, setShowPaymentGate] = useState(false);
  const [paymentConfirmed, setPaymentConfirmed] = useState(false);

  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const attemptId = useRef<number | null>(null);

  // ── Load exam ──────────────────────────────────────────────────────────────
  const startExam = useCallback(async () => {
    try {
      // Check EGP payment before allowing access
      const paymentStatus = await api.getExamPaymentStatus(parseInt(examId)).catch(() => ({ paid: false }));
      if (!paymentStatus.paid) {
        setShowPaymentGate(true);
        setPhase("error");
        setError("exam_payment_required");
        return;
      }
      const data = await api.startExam(parseInt(examId));
      attemptId.current = data.attempt_id;
      setExam(data);
      setTimeLeft(data.duration_minutes * 60);
      setPhase("setup");
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? "Failed to start exam. Please try again.");
      setPhase("error");
    }
  }, [examId]);

  useEffect(() => { startExam(); }, [startExam]);

  // ── Webcam ─────────────────────────────────────────────────────────────────
  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      streamRef.current = stream;
      if (videoRef.current) videoRef.current.srcObject = stream;
      setWebcamOk(true);
    } catch {
      alert("Webcam access is required for this proctored exam.");
    }
  };

  const enterFullscreen = async () => {
    try { await document.documentElement.requestFullscreen(); } catch { /* ignore */ }
    setPhase("active");
    startTimer();
  };

  // ── Timer ──────────────────────────────────────────────────────────────────
  const startTimer = () => {
    timerRef.current = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) { clearInterval(timerRef.current!); handleSubmit(); return 0; }
        return t - 1;
      });
    }, 1000);
  };

  // ── Proctoring ─────────────────────────────────────────────────────────────
  const reportViolation = useCallback(async (type: string, desc: string) => {
    if (!attemptId.current) return;
    try {
      await api.reportViolation(attemptId.current, { violation_type: type, description: desc });
    } catch { /* best-effort */ }
    setViolations((v) => {
      const next = v + 1;
      setViolationMsg(`Violation ${next}/5: ${desc}`);
      setTimeout(() => setViolationMsg(""), 4000);
      if (next >= 5) handleSubmit();
      return next;
    });
  }, []); // eslint-disable-line

  useEffect(() => {
    if (phase !== "active") return;
    const onBlur = () => reportViolation("tab_switch", "Window lost focus");
    const onVis = () => { if (document.hidden) reportViolation("tab_switch", "Tab switched or minimized"); };
    const noCtx = (e: MouseEvent) => e.preventDefault();
    const noKey = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && ["c", "v", "a", "s", "p", "u"].includes(e.key.toLowerCase())) e.preventDefault();
      if (e.key === "F12" || (e.ctrlKey && e.shiftKey && e.key === "I")) e.preventDefault();
    };
    window.addEventListener("blur", onBlur);
    document.addEventListener("visibilitychange", onVis);
    document.addEventListener("contextmenu", noCtx);
    document.addEventListener("keydown", noKey);
    return () => {
      window.removeEventListener("blur", onBlur);
      document.removeEventListener("visibilitychange", onVis);
      document.removeEventListener("contextmenu", noCtx);
      document.removeEventListener("keydown", noKey);
    };
  }, [phase, reportViolation]);

  // ── Submit ─────────────────────────────────────────────────────────────────
  const handleSubmit = useCallback(async () => {
    if (submitting || !attemptId.current) return;
    setSubmitting(true);
    clearInterval(timerRef.current!);
    streamRef.current?.getTracks().forEach((t) => t.stop());
    try { if (document.fullscreenElement) await document.exitFullscreen(); } catch { /* ignore */ }
    try {
      const payload = Object.entries(answers).map(([qid, ans]) => ({
        question_id: parseInt(qid),
        answer: ans,
      }));
      const data = await api.submitExam(attemptId.current, payload);
      setResult(data);
      setPhase("submitted");
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? "Submission failed.");
      setPhase("error");
    }
  }, [answers, submitting]);

  const setAnswer = (qid: number, val: any) => {
    setAnswers((prev) => ({ ...prev, [qid]: val }));
  };

  const answeredCount = exam
    ? exam.questions.filter((q) => {
        const a = answers[q.id];
        if (a === undefined || a === null || a === "") return false;
        if (Array.isArray(a)) return a.length > 0;
        return true;
      }).length
    : 0;

  // ─────────────────────────────────────────────────────────────────────────
  // PHASE: loading
  // ─────────────────────────────────────────────────────────────────────────
  if (phase === "loading") {
    return (
      <div className="min-h-screen bg-void flex items-center justify-center">
        <div className="text-center">
          <Spinner className="w-6 h-6 mx-auto mb-3" />
          <p className="text-xs text-ghost">Preparing exam…</p>
        </div>
      </div>
    );
  }

  // ─────────────────────────────────────────────────────────────────────────
  // PHASE: error
  // ─────────────────────────────────────────────────────────────────────────
  if (phase === "error") {
    if (error === "exam_payment_required") {
      return (
        <div className="min-h-screen bg-void flex items-center justify-center p-6">
          {showPaymentGate && (
            <ExamPaymentGate
              examId={parseInt(examId)}
              examTitle="Certification Exam"
              onPaid={() => { setShowPaymentGate(false); setPaymentConfirmed(true); setPhase("loading"); startExam(); }}
              onClose={() => router.push("/dashboard")}
            />
          )}
          {!showPaymentGate && (
            <Card className="p-8 max-w-md w-full text-center">
              <ShieldCheck size={36} className="text-amber mx-auto mb-4" />
              <h2 className="font-display font-bold text-bright text-lg mb-2">Payment Required</h2>
              <p className="text-sm text-ghost mb-6">This certification exam requires an EGP payment to access.</p>
              <div className="flex gap-3 justify-center">
                <Button onClick={() => setShowPaymentGate(true)}>Pay to Access Exam</Button>
                <Button variant="outline" onClick={() => router.push("/dashboard")}>Go Back</Button>
              </div>
            </Card>
          )}
        </div>
      );
    }
    return (
      <div className="min-h-screen bg-void flex items-center justify-center p-6">
        <Card className="p-8 max-w-md w-full text-center">
          <XCircle size={36} className="text-rose mx-auto mb-4" />
          <h2 className="font-display font-bold text-bright text-lg mb-2">Something went wrong</h2>
          <p className="text-sm text-ghost mb-6">{error}</p>
          <Button onClick={() => router.push("/dashboard")}>Back to Dashboard</Button>
        </Card>
      </div>
    );
  }

  // ─────────────────────────────────────────────────────────────────────────
  // PHASE: submitted
  // ─────────────────────────────────────────────────────────────────────────
  if (phase === "submitted" && result) {
    const passed = result.passed;
    const pct = result.percentage ?? 0;
    return (
      <div className="min-h-screen bg-void flex items-center justify-center p-6">
        <Card className={`p-10 max-w-lg w-full text-center ${passed ? "border-emerald/20" : "border-rose/20"}`}>
          <div className={`w-16 h-16 rounded-full mx-auto mb-5 flex items-center justify-center ${passed ? "bg-emerald/10 border border-emerald/20" : "bg-rose/10 border border-rose/20"}`}>
            {passed ? <Trophy size={28} className="text-emerald" /> : <RotateCcw size={28} className="text-rose" />}
          </div>
          <h1 className="font-display font-bold text-bright text-2xl mb-1">
            {passed ? "Certification Earned!" : "Keep Practicing"}
          </h1>
          <p className="text-sm text-ghost mb-8">{exam?.title}</p>

          <div className="grid grid-cols-4 gap-3 mb-6">
            {[
              { label: "Score", value: result.score },
              { label: "Total", value: result.total_points },
              { label: "Percent", value: `${pct.toFixed(1)}%` },
              { label: "Passing", value: result.passing_score },
            ].map(({ label, value }) => (
              <div key={label} className="bg-surface border border-border rounded-lg p-3">
                <div className={`text-xl font-mono font-bold mb-0.5 ${passed ? "text-emerald" : "text-amber"}`}>{value}</div>
                <div className="text-xs text-ghost">{label}</div>
              </div>
            ))}
          </div>

          <div className="mb-6">
            <ProgressBar value={pct} color={passed ? "emerald" : "rose"} size="md" />
          </div>

          {passed && result.certificate_id && (
            <div className="mb-6 px-4 py-3 bg-emerald/5 border border-emerald/20 rounded-lg">
              <p className="text-xs text-ghost mb-1">Certificate ID</p>
              <code className="text-sm font-mono text-emerald">{result.certificate_id}</code>
            </div>
          )}
          {!passed && (
            <p className="text-sm text-ghost mb-6">
              You need <span className="text-amber font-mono">{result.passing_score}</span> points to pass. Review the material and try again!
            </p>
          )}

          <div className="flex gap-3 justify-center">
            <Button onClick={() => router.push("/dashboard")}>Dashboard</Button>
            {!passed && (
              <Button variant="outline" onClick={() => { setPhase("loading"); startExam(); }}>
                Retry Exam
              </Button>
            )}
          </div>
        </Card>
      </div>
    );
  }

  // ─────────────────────────────────────────────────────────────────────────
  // PHASE: setup
  // ─────────────────────────────────────────────────────────────────────────
  if (phase === "setup" && exam) {
    return (
      <div className="min-h-screen bg-void flex items-center justify-center p-6">
        <div className="max-w-xl w-full space-y-4">
          <div className="text-center mb-6">
            <h1 className="font-display font-bold text-bright text-2xl mb-2">{exam.title}</h1>
            <p className="text-sm text-ghost leading-relaxed">{exam.description}</p>
          </div>

          {/* Meta chips */}
          <div className="flex flex-wrap gap-2 justify-center mb-2">
            {[
              { icon: Clock, label: `${exam.duration_minutes} minutes` },
              { icon: AlignLeft, label: `${exam.questions.length} questions` },
              { icon: Trophy, label: `${exam.total_points} points` },
              { icon: CheckCircle, label: `Pass: ${exam.passing_score}+` },
            ].map(({ icon: Icon, label }) => (
              <span key={label} className="flex items-center gap-1.5 px-3 py-1.5 bg-surface border border-border rounded-lg text-xs text-soft">
                <Icon size={12} className="text-amber" />
                {label}
              </span>
            ))}
          </div>

          {/* Rules */}
          <Card className="p-5">
            <div className="flex items-center gap-2 mb-3">
              <Shield size={14} className="text-amber" />
              <span className="text-xs font-medium text-amber uppercase tracking-widest">Exam Rules</span>
            </div>
            <ul className="space-y-2">
              {[
                "Webcam must remain active throughout the exam",
                "Do not switch tabs or minimize the window",
                "Right-click and developer tools are disabled",
                "Maximum 5 violations before auto-submission",
                "Timer starts when you enter fullscreen",
              ].map((rule) => (
                <li key={rule} className="flex items-start gap-2 text-xs text-ghost">
                  <ChevronRight size={12} className="text-border mt-0.5 flex-shrink-0" />
                  {rule}
                </li>
              ))}
            </ul>
          </Card>

          {/* Webcam */}
          <Card className="p-5">
            <div className="flex items-center gap-2 mb-3">
              <Camera size={14} className="text-amber" />
              <span className="text-xs font-medium text-amber uppercase tracking-widest">Webcam Setup</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-32 h-24 bg-ink border border-border rounded-lg overflow-hidden flex-shrink-0 relative">
                <video ref={videoRef} autoPlay playsInline muted className="w-full h-full object-cover" />
                {!webcamOk && (
                  <div className="absolute inset-0 flex flex-col items-center justify-center gap-1">
                    <Camera size={18} className="text-ghost" />
                    <p className="text-xs text-ghost">No camera</p>
                  </div>
                )}
                {webcamOk && (
                  <div className="absolute top-1.5 right-1.5 flex items-center gap-1 bg-void/80 px-1.5 py-0.5 rounded">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose animate-pulse" />
                    <span className="text-xs font-mono text-rose">REC</span>
                  </div>
                )}
              </div>
              <div>
                {!webcamOk ? (
                  <>
                    <p className="text-sm text-soft mb-2">Camera access required for proctoring.</p>
                    <Button size="sm" variant="outline" onClick={startWebcam}>Enable Camera</Button>
                  </>
                ) : (
                  <div className="flex items-center gap-2">
                    <CheckCircle size={14} className="text-emerald" />
                    <span className="text-sm text-emerald">Camera active</span>
                  </div>
                )}
              </div>
            </div>
          </Card>

          <Button
            className="w-full"
            onClick={webcamOk ? enterFullscreen : undefined}
            disabled={!webcamOk}
          >
            {webcamOk ? "Start Exam — Enter Fullscreen" : "Enable camera to continue"}
          </Button>
        </div>
      </div>
    );
  }

  // ─────────────────────────────────────────────────────────────────────────
  // PHASE: active
  // ─────────────────────────────────────────────────────────────────────────
  if (phase === "active" && exam) {
    const q = exam.questions[current];
    const ans = answers[q.id];
    const progress = (answeredCount / exam.questions.length) * 100;
    const danger = timeLeft < 300;
    const meta = TYPE_META[q.question_type] ?? TYPE_META.short;
    const TypeIcon = meta.icon;

    return (
      <div className="flex h-screen bg-void overflow-hidden" style={{ userSelect: "none" }}>

        {/* Violation toast */}
        {violationMsg && (
          <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 px-4 py-2.5 bg-ink border border-amber/40 rounded-lg shadow-xl">
            <AlertTriangle size={13} className="text-amber" />
            <span className="text-xs text-amber font-medium">{violationMsg}</span>
          </div>
        )}

        {/* ── Sidebar ── */}
        <aside className="w-52 shrink-0 flex flex-col bg-ink border-r border-border overflow-y-auto">
          {/* Brand */}
          <div className="px-4 py-4 border-b border-border">
            <p className="text-xs font-medium text-bright truncate">{exam.title}</p>
            <p className="text-xs text-ghost mt-0.5">{answeredCount}/{exam.questions.length} answered</p>
          </div>

          {/* Progress */}
          <div className="px-4 py-3 border-b border-border">
            <ProgressBar value={progress} size="sm" />
          </div>

          {/* Q grid */}
          <div className="p-3 flex-1">
            <p className="text-xs text-ghost uppercase tracking-widest mb-2 font-medium">Questions</p>
            <div className="grid grid-cols-4 gap-1.5">
              {exam.questions.map((sq, i) => {
                const a = answers[sq.id];
                const done = Array.isArray(a) ? a.length > 0 : !!(a);
                return (
                  <button
                    key={sq.id}
                    onClick={() => setCurrent(i)}
                    title={`Q${i + 1}: ${TYPE_META[sq.question_type]?.label}`}
                    className={`aspect-square rounded text-xs font-mono transition-all duration-150 ${
                      i === current
                        ? "bg-amber/20 border border-amber/50 text-amber"
                        : done
                        ? "bg-emerald/10 border border-emerald/30 text-emerald"
                        : "bg-surface border border-border text-ghost hover:border-amber/20 hover:text-soft"
                    }`}
                  >
                    {i + 1}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Webcam */}
          <div className="p-3 border-t border-border">
            <div className="relative rounded-lg overflow-hidden border border-border bg-void">
              <video ref={videoRef} autoPlay playsInline muted className="w-full block" />
              <div className="absolute top-1.5 right-1.5 flex items-center gap-1 bg-void/80 px-1.5 py-0.5 rounded">
                <span className="w-1.5 h-1.5 rounded-full bg-rose animate-pulse" />
                <span className="text-xs font-mono text-rose">REC</span>
              </div>
            </div>
          </div>
        </aside>

        {/* ── Main ── */}
        <div className="flex-1 flex flex-col overflow-hidden">

          {/* Top bar */}
          <header className="h-14 flex items-center justify-between px-6 bg-ink border-b border-border flex-shrink-0">
            <div className="flex items-center gap-2">
              <TypeIcon size={14} className="text-ghost" />
              <Badge variant={meta.variant as any}>{meta.label}</Badge>
              <span className="text-xs text-ghost font-mono ml-1">{q.points} pts</span>
            </div>
            <div className="flex items-center gap-3">
              {violations > 0 && (
                <span className="flex items-center gap-1.5 text-xs text-amber bg-amber/10 border border-amber/20 px-2.5 py-1 rounded-full">
                  <AlertTriangle size={11} />
                  {violations}/5 violations
                </span>
              )}
              <div className={`flex items-center gap-1.5 font-mono text-sm font-bold px-3 py-1.5 rounded-lg border ${
                danger
                  ? "text-rose bg-rose/10 border-rose/30 animate-pulse"
                  : "text-bright bg-surface border-border"
              }`}>
                <Clock size={13} />
                {fmtTime(timeLeft)}
              </div>
              <Button size="sm" variant="outline" onClick={handleSubmit} disabled={submitting}>
                {submitting ? <Spinner className="w-3 h-3" /> : "Submit"}
              </Button>
            </div>
          </header>

          {/* Question */}
          <main className="flex-1 overflow-y-auto px-8 py-8 max-w-3xl w-full mx-auto">
            <div className="mb-2">
              <span className="text-xs font-mono text-ghost">Q{current + 1} of {exam.questions.length}</span>
            </div>
            <h2 className="text-lg font-medium text-bright leading-relaxed mb-7">{q.question_text}</h2>

            <div className="mb-10">
              {q.question_type === "mcq" && (
                <MCQ q={q} value={ans as string ?? ""} onChange={(v) => setAnswer(q.id, v)} />
              )}
              {q.question_type === "multi" && (
                <MultiChoice q={q} value={(ans as string[]) ?? []} onChange={(v) => setAnswer(q.id, v)} />
              )}
              {q.question_type === "true_false" && (
                <TrueFalse value={ans as string ?? ""} onChange={(v) => setAnswer(q.id, v)} />
              )}
              {q.question_type === "code" && (
                <CodeEditor q={q} value={ans as string ?? ""} onChange={(v) => setAnswer(q.id, v)} />
              )}
              {q.question_type === "fill_blank" && (
                <FillBlank q={q} value={(ans as string[]) ?? []} onChange={(v) => setAnswer(q.id, v)} />
              )}
              {q.question_type === "ordering" && (
                <Ordering q={q} value={(ans as string[]) ?? []} onChange={(v) => setAnswer(q.id, v)} />
              )}
              {q.question_type === "short" && (
                <ShortAnswer value={ans as string ?? ""} onChange={(v) => setAnswer(q.id, v)} />
              )}
            </div>

            {/* Nav */}
            <div className="flex items-center justify-between pt-4 border-t border-border">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrent((c) => Math.max(0, c - 1))}
                disabled={current === 0}
              >
                <ChevronLeft size={14} /> Previous
              </Button>
              {current < exam.questions.length - 1 ? (
                <Button
                  size="sm"
                  onClick={() => setCurrent((c) => c + 1)}
                >
                  Next <ChevronRight size={14} />
                </Button>
              ) : (
                <Button
                  size="sm"
                  onClick={handleSubmit}
                  disabled={submitting}
                  className="bg-emerald text-void hover:bg-emerald/90"
                >
                  {submitting ? <Spinner className="w-3 h-3" /> : <><CheckCircle size={14} /> Submit Exam</>}
                </Button>
              )}
            </div>
          </main>
        </div>
      </div>
    );
  }

  return null;
}
