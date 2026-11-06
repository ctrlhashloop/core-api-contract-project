# API Contract Testing Project

### Here is how to set it up step by step:

1. Create and Navigate to the Pact Directory
(_Set up the monorepo workspace and install required tools_)
    - Open your terminal, navigate to your  project root, create a dedicated pact/ folder, and initialize a new Node.js project:

    ```
    mkdir pact
    cd pact
    npm init -y             # Initialize project directory
                            # creates package.json file
    ```

2.  Install Typescript, Jest and Pact JS     
    
    - Install TypeScript, Jest (along with ts-jest for running TypeScript tests), and the Pact V3 library as development dependencies:
    - This Installs the  runtime and testing dependencies

    ```
    npm install --save-dev typescript jest ts-jest @types/jest @pact-foundation/pact
    ```

3. Generate tsconfig.json

   (_Configure TypeScript compilation_)
   - Initialize a TypeScript configuration file for your consumer tests:

        ```npx tsc --init```         
   - Verification: Run npx tsc --noEmit to verify that TypeScript compiles without syntax errors.

4. Initialize Jest Configuration

    (_Configure Jest test runner_)
   - Configure Jest to use ts-jest for compiling and executing TypeScript test files. Run the initialization command: 
   ```npx ts-jest config:init```
   - This creates a jest.config.js file. Verify it includes preset: 'ts-jest'.
   - Verification: Add a test script to your package.json:

     ``` "test": "jest" ```
   - Then run npm test to confirm Jest executes successfully.  

5. Define the API Contract (OpenAPI 3.0) 
(_Establish the single source of truth before writing code_)

    - Create openapi/openapi.yaml. This YAML file defines the exact endpoints, request payloads, response schemas, and status codes that both teams agree upon:

6. Write Consumer-Driven Contracts (TypeScript & Pact)
(_Capture frontend/client expectations and generate Pact JSON files_) 

    - Inside the pact/ directory, write a consumer contract test using Pact. This simulates how the client calls the API and generates a contract file (.json).
    - Execution: Run npm test to validate the client code and output the contract JSON file to pacts/webfrontendclient-corebankingservice.json.

7. Implement the Provider Backend (FastAPI & Pydantic)
    - 4.Implement the Provider Backend (FastAPI & Pydantic):Build the Python service matching the OpenAPI specification.
    - Inside server/main.py, implement the FastAPI application matching the exact data structures specified in the contract:
    - Inside server folder run: 
        ```pip install fastapi uvicorn pytest```

8. Execution: Start the server locally using Uvicorn:
    - Navigate to the root directory 
    ```uvicorn server.main:app --reload --port 8000```  

9. Verify the Provider against the Contract (Pytest)
(_Automate backend verification using Pact and Pytest_)
    - Inside tests/test_contract_provider.py, configure Pact-Python to spin up the FastAPI app and verify that it satisfies the consumer's expectations:    
    - Execution: Run pytest to verify the provider:
    ``` pytest tests/test_contract_provider.py -v ```      

### Common Errors
1. Cannot find module './client' or its corresponding type declarations.
    - This error occurs because TypeScript cannot find the client.ts file in your pact/ directory, or because the axios HTTP client dependency required by the client has not been installed yet.
    - Here is how to resolve it:
    (_Step 1: Install Axios in the Pact Directory_) 
    ```Install Axios in the Pact Directory:Install Axios dependency.Ensure you are inside your pact/ folder and install axios so your HTTP client can make requests to the mock server: npm install axios ```  
    (_Step 2:_: Create the API Client File:)
    ```Create client.ts file.Create a file named client.ts directly inside your pact/ directory (making sure it sits side-by-side with consumer.test.ts):``` 


    ```npm install --save-dev typescript@^5.3.3 --legacy-peer-deps```