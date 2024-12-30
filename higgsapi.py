from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Scaling Factor
SCALING_FACTOR = 27075.00

# Input models
class EnergyInput(BaseModel):
    energy: float

class SignalInput(BaseModel):
    raw_signal: float

class SimulationInput(BaseModel):
    data_points: list[float]

# Endpoints
@app.post("/scale-energy")
def scale_energy(input: EnergyInput):
    """
    Scale energy levels using the predefined scaling factor.
    """
    scaled_energy = input.energy * SCALING_FACTOR
    return {"scaled_energy": scaled_energy}

@app.post("/calibrate-detector")
def calibrate_detector(input: SignalInput):
    """
    Calibrate detector sensitivity based on the scaling factor.
    """
    calibrated_signal = input.raw_signal / SCALING_FACTOR
    return {"calibrated_signal": calibrated_signal}

@app.post("/refine-simulation")
def refine_simulation(input: SimulationInput):
    """
    Refine simulation parameters using the scaling factor.
    """
    refined_data = [point * SCALING_FACTOR for point in input.data_points]
    return {"refined_data": refined_data}