from ranx import Qrels, Run, evaluate, compare
from rich.console import Console
from rich.table import Table

def load_questions(questions_file):
  return Qrels.from_file(questions_file)


def create_run(questions, retrieval_fn, name):
  run_dict = {
    question: {
      str(index): score
      for index, score in (retrieval_fn(question)
                            .select("index, score")
                            .fetchall()
                          )
    }
    for question in questions.to_dict()
  }
  return Run(run_dict, name=name)

def as_run(run_dict, name):
  return Run(run_dict, name)


def compare_table(qrels, runs):
  table = Table(title="Comparing Retrieval Techniques")
  table.add_column("Question")
  for run in runs:
    table.add_column(run.name, justify="center")

  cols = [col.header for col in table.columns][1:]
  for question in qrels.to_dict():
    row = [question]
    for col in cols:
      selected_run = [r for r in runs if r.name == col][0]
      score = selected_run.scores['hit_rate'][question]
      row.append("✅" if score == 1.0 else "❌")
    table.add_row(*row)
  return table