From sklearn website:
1 Epoch = 1 Forward pass + 1 Backward pass for ALL training samples.
Batch Size = Number of training samples in 1 Forward/1 Backward pass. (With increase in Batch size, required memory space increases.)
Number of iterations = Number of passes i.e. 1 Pass = 1 Forward pass + 1 Backward pass (Forward pass and Backward pass are not counted differently.)

Example : If we have 1000 training samples and Batch size is set to 500, it will take 2 iterations to complete 1 Epoch.