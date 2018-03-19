import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

public class TxHandler {

    UTXOPool utxoPool;

    /**
     * Creates a public ledger whose current UTXOPool (collection of unspent transaction outputs) is
     * {@code utxoPool}. This should make a copy of utxoPool by using the UTXOPool(UTXOPool uPool)
     * constructor.
     */
    public TxHandler(UTXOPool utxoPool) {
        this.utxoPool = new UTXOPool(utxoPool);
    }

    /**
     * @return true if:
     * (1) all outputs claimed by {@code tx} are in the current UTXO pool,
     * (2) the signatures on each input of {@code tx} are valid,
     * (3) no UTXO is claimed multiple times by {@code tx},
     * (4) all of {@code tx}s output values are non-negative, and
     * (5) the sum of {@code tx}s input values is greater than or equal to the sum of its output
     *     values; and false otherwise.
     */
    public boolean isValidTx(Transaction tx) {
        // (1) all outputs claimed by {@code tx} are in the current UTXO pool,
        for (Transaction.Input in : tx.getInputs()) {
            UTXO utxo = new UTXO(in.prevTxHash, in.outputIndex);
            if (!utxoPool.contains(utxo)) {
                return false;
            }
        }

        // (2) the signatures on each input of {@code tx} are valid,
        for (int i = 0; i < tx.numInputs(); i++) {
            Transaction.Input in = tx.getInput(i);

            UTXO utxo = new UTXO(in.prevTxHash, in.outputIndex);
            Transaction.Output prevOut = utxoPool.getTxOutput(utxo);
            if (prevOut != null) {
                byte[] message = tx.getRawDataToSign(i);
                if (!Crypto.verifySignature(prevOut.address, message, in.signature)) {
                    return false;
                }
            }
        }

        // (3) no UTXO is claimed multiple times by {@code tx},
        Set<UTXO> claimed = new HashSet<UTXO>();
        for (Transaction.Input in : tx.getInputs()) {
            UTXO utxo = new UTXO(in.prevTxHash, in.outputIndex);
            if (claimed.contains(utxo)) {
                return false;
            }
            claimed.add(utxo);
        }

        // (4) all of {@code tx}s output values are non-negative, and
        for (Transaction.Output out : tx.getOutputs()) {
            if (out.value < 0) {
                return false;
            }
        }

        // (5) the sum of {@code tx}s input values is greater than or equal to
        //     the sum of its output values; and false otherwise.
        double sumInput = 0;
        for (Transaction.Input in : tx.getInputs()) {
            UTXO utxo = new UTXO(in.prevTxHash, in.outputIndex);
            Transaction.Output out = utxoPool.getTxOutput(utxo);
            if (out != null) {
                sumInput += out.value;
            }
        }

        double sumOutput = 0;
        for (Transaction.Output out : tx.getOutputs()) {
            sumOutput += out.value;
        }

        return sumInput >= sumOutput;
    }

    /**
     * Handles each epoch by receiving an unordered array of proposed transactions, checking each
     * transaction for correctness, returning a mutually valid array of accepted transactions, and
     * updating the current UTXO pool as appropriate.
     */
    public Transaction[] handleTxs(Transaction[] possibleTxs) {
        ArrayList<Transaction> valids = new ArrayList<Transaction>();
        for (Transaction tx : possibleTxs) {
            if (!isValidTx(tx)) {
                continue;
            }

            valids.add(new Transaction(tx));
            for (Transaction.Input in : tx.getInputs()) {
                UTXO utxo = new UTXO(in.prevTxHash, in.outputIndex);
                utxoPool.removeUTXO(utxo);
            }

            byte[] txHash = tx.getHash();
            for (int i = 0; i < tx.numOutputs(); i++) {
                UTXO utxo = new UTXO(txHash, i);
                Transaction.Output out = tx.getOutput(i);
                utxoPool.addUTXO(utxo, out);
            }
        }
        return valids.toArray(new Transaction[valids.size()]);
    }

}
