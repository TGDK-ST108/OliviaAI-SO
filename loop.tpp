 // T++ - Loop Handler for Code Execution

class LoopHandler {
    var counter;
    var maxIterations;

    // Initialize LoopHandler with Max Iterations
    def LoopHandler(maxIterations) {
        this.counter = 0;
        this.maxIterations = maxIterations;
    }

    // Function to Execute a Loop
    def executeLoop() {
        while (this.counter < this.maxIterations) {
            print("Iteration: " + this.counter);
            this.counter += 1;
        }
        return "Loop Execution Completed.";
    }
}

// Initialize Loop Handler with 10 Iterations
LoopHandler loop = new LoopHandler(10);

// Run the Loop
print(loop.executeLoop());