import indra
import macros
import predicate

def make_predicate_many(statements):
    if len(statements) == 0:
        return predicate.Top()
    elif len(statements) == 1:
        return make_predicate(statements[0])
    else:
        predicates = [make_predicate(statement) for statement in statements]
        return predicate.And(*predicates)

def make_predicate(statement):
    if isinstance(statement, indra.statements.Phosphorylation):
        # <enzyme> phosphorylates <substrate>
        # str() because sometimes these are Unicode
        enzyme = str(statement.enz.name)
        substrate = str(statement.sub.name)
        return macros.directly_phosphorylates(enzyme, substrate)
    elif isinstance(statement, indra.statements.ActivityActivity):
        # <enzyme> activates <substrate>
        upstream = str(statement.subj.name)
        downstream = str(statement.obj.name)
        if statement.subj_activity == 'act' and statement.obj_activity == 'act':
            return macros.directly_activates(upstream, downstream)
        else:
            raise NotImplementedError(str(statement))
    # TODO: ActivityModification macro -- I can't get an INDRA example
    # to test by, but it will be very similar to the above.

    raise NotImplementedError(str(statement))