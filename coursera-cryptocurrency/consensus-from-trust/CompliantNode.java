import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

/* CompliantNode refers to a node that follows the rules (not malicious)*/
public class CompliantNode implements Node {

    private Set<Transaction> transactions;

    private boolean[] followees;

    public CompliantNode(double p_graph, double p_malicious, double p_txDistribution, int numRounds) {
        transactions = new HashSet<Transaction>();
    }

    public void setFollowees(boolean[] followees) {
        this.followees = followees;
    }

    public void setPendingTransaction(Set<Transaction> pendingTransactions) {
        this.transactions.addAll(pendingTransactions);
    }

    public Set<Transaction> sendToFollowers() {
        return this.transactions;
    }

    public void receiveFromFollowees(Set<Candidate> candidates) {
        for (Candidate c : candidates) {
            if (this.followees[c.sender]) {
                this.transactions.add(c.tx);
            }
        }
    }
}
