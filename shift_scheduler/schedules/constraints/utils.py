"""Module that helps build constraints."""

from ortools.sat.python import cp_model


def create_soft_constraint(
    model: cp_model.CpModel,
    events: list[cp_model.IntVar],
    soft_min: int | None = None,
    soft_max: int | None = None,
    penalty_per_unit: int = 1,
) -> cp_model.ObjLinearExprT:
    """
    Create a linear expression that represents the penalties
    when the number of truthful `events` exceeds the soft bound.
    """

    value = model.new_int_var(0, len(events), name="")
    model.add(sum(events) == value)

    penalty_expression: cp_model.ObjLinearExprT = 0

    if soft_min is not None and penalty_per_unit > 0:
        difference = model.new_int_var(-len(events), len(events), name="")
        violation = model.new_int_var(0, len(events), name="")

        model.add(difference == soft_min - value)
        model.add_max_equality(violation, (0, difference))

        penalty_expression += violation * penalty_per_unit

    if soft_max is not None and penalty_per_unit > 0:
        difference = model.new_int_var(-len(events), len(events), name="")
        violation = model.new_int_var(0, len(events), name="")

        model.add(difference == value - soft_max)
        model.add_max_equality(violation, (0, difference))

        penalty_expression += violation * penalty_per_unit

    return penalty_expression
