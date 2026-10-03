"""Autonomous agent REPL: Plan -> Execute -> Evaluate -> Replan (up to 3 iterations)."""

from colorama import Fore, Style, init

from evaluator import Evaluator
from executor import Executor
from planner import Planner


def print_plan(plan: list[dict]) -> None:
    """Print full plan in a readable format."""
    print(Fore.MAGENTA + "\n[Planning] Generated Plan:" + Style.RESET_ALL)
    for step in plan:
        print(
            Fore.MAGENTA
            + f"  {step['step_number']}. {step['description']}"
            + Style.RESET_ALL
        )
        print(Fore.MAGENTA + f"     -> {step['expected_output']}" + Style.RESET_ALL)


def run_agent(goal: str, max_iterations: int = 3) -> dict:
    """Run the full autonomous loop for a goal and return the final evaluation."""
    planner, executor, evaluator = Planner(), Executor(), Evaluator()
    feedback, final_eval = None, {"success": False, "feedback": "", "summary": ""}

    for iteration in range(1, max_iterations + 1):
        print(Fore.MAGENTA + f"\n[Planning] Iteration {iteration}" + Style.RESET_ALL)
        plan = planner.create_plan(goal, feedback)
        print_plan(plan)

        results = []
        for step in plan:
            print(
                Fore.CYAN
                + f"\n[Executing] Step {step['step_number']}: {step['description']}"
                + Style.RESET_ALL
            )
            result = executor.execute_step(step, context=goal)
            results.append(result)
            print(Fore.GREEN + f"[Result] {result}\n" + Style.RESET_ALL)

        print(Fore.YELLOW + "[Evaluating] Assessing progress..." + Style.RESET_ALL)
        final_eval = evaluator.evaluate(goal, results)
        print(Fore.YELLOW + f"[Evaluation] {final_eval['summary']}" + Style.RESET_ALL)

        if final_eval["success"]:
            print(Fore.GREEN + "\n[Result] Goal achieved." + Style.RESET_ALL)
            return final_eval

        feedback = final_eval.get("feedback", "Need a better plan.")
        print(Fore.YELLOW + f"[Evaluation] Replanning feedback: {feedback}" + Style.RESET_ALL)

    print(Fore.GREEN + "\n[Result] Max iterations reached." + Style.RESET_ALL)
    return final_eval


def repl() -> None:
    """Interactive shell for submitting high-level goals."""
    init(autoreset=True)
    print("Autonomous Agent REPL. Type /quit to exit.")
    while True:
        goal = input("\nGoal> ").strip()
        if not goal:
            continue
        if goal.lower() == "/quit":
            print("Exiting.")
            break
        run_agent(goal)


if __name__ == "__main__":
    repl()
