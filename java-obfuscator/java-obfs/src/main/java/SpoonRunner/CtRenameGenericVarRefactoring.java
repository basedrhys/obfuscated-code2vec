package SpoonRunner;

import spoon.refactoring.AbstractRenameRefactoring;
import spoon.reflect.declaration.CtVariable;
import spoon.reflect.reference.CtReference;
import spoon.reflect.visitor.chain.CtConsumer;
import spoon.reflect.visitor.filter.VariableReferenceFunction;

public class CtRenameGenericVarRefactoring extends AbstractRenameRefactoring<CtVariable> {

    public CtRenameGenericVarRefactoring() {
        super(javaIdentifierRE);
    }

    @Override
    protected void refactorNoCheck() {
        getTarget().map(new VariableReferenceFunction()).forEach(new CtConsumer<CtReference>() {
            @Override
            public void accept(CtReference t) {
                t.setSimpleName(newName);
            }
        });
        target.setSimpleName(newName);
    }
}
