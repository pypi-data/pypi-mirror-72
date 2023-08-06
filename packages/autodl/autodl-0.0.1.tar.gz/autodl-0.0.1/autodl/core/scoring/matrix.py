import os
import yaml
import pandas as pd

class Matrix:
  """Matrix object based on a pandas.DataFrame object.

    Args:
        matrix_path (str, optional): path to csv file of a matrix to load. Defaults to None.
        scores_files (list, optional): path to a list of scores.txt files to add to the current matrix. Defaults to None.
    """
  def __init__(self, matrix_path: str=None, scores_files: list=None):
    self.matrix_path = matrix_path # path to previous matrix
    if matrix_path is not None and os.path.exists(matrix_path):
      self.load_matrix(matrix_path)
    else:
      self.df = pd.DataFrame()
    self.init_execution_id()
    self.add_scores_files(scores_files)

  def init_execution_id(self):
    if len(self.df) == 0:
      self.execution_id = 0
    else:
      self.execution_id = max(self.df['execution_id'])

  def refresh_execution_id(self):
    self.execution_id = self.execution_id + 1

  def load_matrix(self, matrix_path):
    if os.path.exists(matrix_path):
      self.df = pd.read_csv(matrix_path)
    else:
      print(f"Could load {matrix_path} because the file does not exist!")

  def to_csv(self, path: str):
    """Save matrix as a CSV format at the given path.

    Args:
        path (str): path of the file to save.
    """
    self.df.to_csv(path, index=False)

  def add_scores(self, path_to_scores: str):
    """Add a scores.txt to the matrix.

    Args:
        path_to_scores (str): path to the scores.txt file to add.
    """
    if os.path.exists(path_to_scores):

      with open(path_to_scores, "r") as f:
        scores = yaml.safe_load(f)
      scores['execution_id'] = self.execution_id
      sub_df = pd.DataFrame(scores)
      self.df = pd.concat([self.df, sub_df], sort=True, ignore_index=True)
      self.refresh_execution_id()

    else:
      print(f"File {path_to_scores} was not added to matrix because the file does not exist!")


  def add_scores_files(self, scores_files: list):
    """Add a list of scores.txt to the matrix.

    Args:
        scores_files (list): list of path to scores.txt files to add.
    """
    for path_to_scores in scores_files:
      self.add_scores(path_to_scores)

if __name__ == '__main__':
  matrix = Matrix(
    matrix_path="mymatrix.csv",
    scores_files=[
      "/Users/evariste/projects/autodl-benchmark/autodl/core/AutoDL_scoring_output/scores.txt",
      "/Users/evariste/projects/autodl-benchmark/autodl/core/AutoDL_scoring_output/scores.txt",
      "/Users/evariste/projects/autodl-benchmark/autodl/core/AutoDL_scoring_output/scores.txt",
    ]
  )

  matrix.to_csv("mymatrix.csv")