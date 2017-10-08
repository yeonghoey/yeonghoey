import java.security.KeyPairGenerator;
import java.security.PublicKey;
import java.security.NoSuchAlgorithmException;

class ScroogeCoin {
    public static void main(String[] args) {
        test1();
        test2();

        System.out.println("Done");
    }

    public static void test1() {
        UTXOPool utxoPool = new UTXOPool();
        TxHandler txHandler = new TxHandler(utxoPool);
        Transaction tx = new Transaction();
        assert !txHandler.isValidTx(tx);
    }

    public static void test2() {
        // Transaction tx = new Transaction();
        // tx2.setHash(new byte[0]);
        // tx2.addOutput(100, createPublicKey());
        // assert !txHandler.isValidTx(tx2);

    }

    public static PublicKey createPublicKey() {
        try {
            KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
            keyGen.initialize(1024);
            return keyGen.genKeyPair().getPublic();
        } catch (NoSuchAlgorithmException e) {
            return null;
        }
    }
}
