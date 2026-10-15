The previous CACE template failed because `iterations` only appeared in a
comment. CACE discovers conditions by scanning active template placeholders,
so it reported "No conditions found" and then could not collate on iterations.

This version contains the active statement

    .param cace_iteration=CACE{iterations}

which makes `iterations` a real template condition.  The parameter is otherwise
unused electrically; its sole purpose is to let CACE enumerate and collate 500
independent mismatch runs.

Run from the JanteStroemSpejl project directory:

    cace cace/JanteStroemSpejl.yaml --source schematic -j 8

Expected early log messages include recognition of the `iterations` condition
and "Collating results using condition \"iterations\"" without the previous
"Couldn't find condition" error.
