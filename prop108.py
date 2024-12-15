class Proposal:
    def __init__(self, proposal_data):
        self.data = proposal_data
        self.status = 'Pending'

    def evaluate_impact(self, system_data):
        # Machine learning model to predict impact
        prediction = model.predict(self.data)
        if prediction['performance_impact'] < 0.2:  # Low impact
            self.status = 'Approved'
        else:
            self.status = 'Needs Review'

def process_proposals(proposals, system_data):
    for proposal in proposals:
        proposal.evaluate_impact(system_data)