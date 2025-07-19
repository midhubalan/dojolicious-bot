from typing import Iterable
from antchat import AntChat
from chattypehelpers import Task, Content, EvalRecord


class EvalRunner:
    def __init__(
        self, *, prompt: str | None = None, cases: Iterable[Task] | None = None
    ) -> None:
        self._chat = AntChat()
        self._prompt = prompt
        self._cases = cases
        self._records:list[EvalRecord] = []

    def _run_prompt(self, case: Task) -> Content:
        if not (self._prompt and self._cases):
            raise ValueError("provide values for prompt and cases")
        self._chat.reset()
        self._chat.add_user_message(self._prompt.format(**case))
        # self._chat.send_messages(stop_sequences=["```"])
        self._chat.send_messages()
        resp = self._chat.get_last_response()
        self._chat.reset()
        return resp

    def _run_eval(self, case: Task) -> EvalRecord:
        resp = self._run_prompt(case)
        return {"output": resp, "test_case": case, "score": 10}

    def run_evals(self) -> None:
        if not self._cases:
            raise ValueError("provide values for cases")
        for case in self._cases:
            self._records.append(self._run_eval(case))
    def get_evals(self) -> Iterable[EvalRecord]:
        if len(self._records) == 0:
            raise ValueError("No records. did you run an eval?")
        return (item for item in self._records)
