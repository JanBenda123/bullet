from django.db import models
from django.db.models import UniqueConstraint


class Problem(models.Model):
    competition = models.ForeignKey(
        "competitions.Competition", on_delete=models.CASCADE, related_name="+"
    )
    name = models.CharField(max_length=128)


class CategoryProblem(models.Model):
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="category_problems"
    )
    category = models.ForeignKey(
        "competitions.CategoryCompetition",
        on_delete=models.CASCADE,
        related_name="problems",
    )
    number = models.PositiveIntegerField()

    class Meta:
        constraints = (
            UniqueConstraint(
                "problem",
                "category",
                "number",
                name="categoryproblem__problem_category_number",
            ),
        )


class SolvedProblem(models.Model):
    team = models.ForeignKey(
        "users.Team", on_delete=models.CASCADE, related_name="solved_problems"
    )
    problem = models.ForeignKey(Problem, on_delete=models.RESTRICT, related_name="+")
    competition_time = models.DurationField()


class ScannerLog(models.Model):
    class Result(models.IntegerChoices):
        OK = 0
        SCAN_ERR = 1
        INTEGRITY_ERR = 2

    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    barcode = models.CharField(max_length=32)
    result = models.IntegerField(choices=Result.choices)
    message = models.CharField(max_length=128, blank=True)
    timestamp = models.DateTimeField()


class ResultRow(models.Model):
    team = models.ForeignKey("users.Team", on_delete=models.CASCADE, related_name="+")
    competition_time = models.DurationField()
    solved_problems = models.BinaryField()
    solved_count = models.IntegerField()

    def get_squares(self, problem_count, team_problem_count):
        squares = []
        solved = int.from_bytes(self.solved_problems, "big")

        for i in range(problem_count):
            st = 0
            if solved & (1 << i):
                st = 2
            elif i < self.solved_count + team_problem_count:
                st = 1

            squares.append(st)

        return squares
