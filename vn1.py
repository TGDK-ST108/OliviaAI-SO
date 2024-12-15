class ValidatorNode:
    def __init__(self, node_id, public_key):
        self.node_id = node_id
        self.public_key = public_key
        self.vote = None

    def validate_proposal(self, proposal):
        if proposal.meets_criteria():
            self.vote = "Approve"
        else:
            self.vote = "Reject"

def reach_consensus(validators, proposal):
    votes = [validator.validate_proposal(proposal) for validator in validators]
    return "Approved" if votes.count("Approve") > len(votes) / 2 else "Rejected"