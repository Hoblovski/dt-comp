"""
Generator parameters.

Note some fine-tweaking algorithms are hard-coded e.g. literal value.
"""
class Config:
    MaxBlockStmt = 10
    MaxBlockDepth = 7

    MaxExprDepth = 8

    # When generating if stmt, the probability of generating an else clause in percentage
    IfStmtWithElseProb = 60

    # When generating expr stmt, the probability of generating an assignment
    ExprStmtAssign = 90

    class StmtWeights:
        # Weights of statements. Bigger indicate more likely.
        # On reaching MaxBlockDepth, weights of nested stmt become 0.
        ExprW = 10
        ReturnW = 1
        BlockW = 3
        IfW = 3

    class ExprWeights:
        # On reaching MaxExprDepth, weights of nested stmt become 0.
        LitW = 1
        BinaryW = 2
        UnaryW = 1
        AssignW = 1
        VarW = 2

