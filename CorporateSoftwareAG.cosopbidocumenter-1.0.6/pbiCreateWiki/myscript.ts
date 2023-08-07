import tl = require('azure-pipelines-task-lib');
import { spawn } from 'child_process';
const exec = require('child_process').exec;

const installPythonPackages = (reqPath: string) => {
    return new Promise((resolve, reject) => {
        // Replace with the correct path to your requirements.txt file
        const command = "pip3 install -r " + reqPath;

        exec(command, (error: Error, stdout: string, stderr: string) => {
            if (error) {
                console.error(`exec error: ${error}`);
                reject(error);
            } else {
                console.log(`Packages installed successfully: ${stdout}`);
                resolve(stdout);
            }
        });
    });
}

// Function to execute python script
const runScript = (scriptPath: string, args: string[]): Promise<string> => {
    return new Promise((resolve, reject) => {
        const process = spawn('python3', [scriptPath, ...args]);

        let scriptOutput: string = "";

        process.stdout.on('data', (data: Buffer) => {
            console.log('stdout: ', data.toString());
            scriptOutput += data.toString();
        });

        process.on('error', (error: Error) => {
            console.log('error: ', error.stack);
            reject(error);
        });

        process.on('exit', (code: number) => {
            console.log('child process exited with code ', code);
            console.log('Script output:', scriptOutput);
            resolve(scriptOutput);
        });
    });
}

async function run() {
    try {
        const workingDirectory = tl.getVariable('System.DefaultWorkingDirectory') || "";
        const pat = tl.getVariable('pat') || "";

        const path = require('path');
        const scriptPath = path.join(__dirname, 'python/create-wiki.py');

        console.log("Working directory: " + workingDirectory);
        console.log("Script path: " + scriptPath);
        const dep = await installPythonPackages(path.join(__dirname, 'python/requirements.txt'));
        // Run the python script with input as argument
        const data = await runScript(scriptPath, [workingDirectory, pat]);
        console.log(data);
    }
    catch (err) {
        tl.setResult(tl.TaskResult.Failed, (err as Error).message);
    }
}

run();
