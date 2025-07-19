from typing import Iterable
from .antchat import AntChat
from .types import Task, Content, EvalRecord


class EvalRunner:
    def __init__(
        self, *, prompt: str | None = None, cases: Iterable[Task] | None = None
    ) -> None:
        self._chat = AntChat()
        self._prompt = prompt
        self._cases = cases

    def _run_prompt(self, case: Task) -> Content:
        if not (self._prompt and self._cases):
            raise ValueError("provide values for prompt and cases")
        self._chat.reset()
        self._chat.add_user_message(self._prompt.format(**case))
        self._chat.send_messages(stop_sequences=["```"])
        resp = self._chat.get_last_response()
        self._chat.reset()
        return resp

    def _run_eval(self, case: Task) -> EvalRecord:
        resp = self._run_prompt(case)
        return {"output": resp, "test_case": case, "score": 10}

    def run_evals(self) -> Iterable[EvalRecord]:
        if not self._cases:
            raise ValueError("provide values for cases")
        results: list[EvalRecord] = []
        for case in self._cases:
            results.append(self._run_eval(case))
        return results
