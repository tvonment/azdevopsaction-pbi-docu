"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const tl = require("azure-pipelines-task-lib");
const child_process_1 = require("child_process");
const exec = require('child_process').exec;
const installPythonPackages = (reqPath) => {
    return new Promise((resolve, reject) => {
        // Replace with the correct path to your requirements.txt file
        const command = "pip3 install -r " + reqPath;
        exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                reject(error);
            }
            else {
                console.log(`Packages installed successfully: ${stdout}`);
                resolve(stdout);
            }
        });
    });
};
// Function to execute python script
const runScript = (scriptPath, args) => {
    return new Promise((resolve, reject) => {
        const process = (0, child_process_1.spawn)('python3', [scriptPath, ...args]);
        let scriptOutput = "";
        process.stdout.on('data', (data) => {
            console.log('stdout: ', data.toString());
            scriptOutput += data.toString();
        });
        process.on('error', (error) => {
            console.log('error: ', error.stack);
            reject(error);
        });
        process.on('exit', (code) => {
            console.log('child process exited with code ', code);
            console.log('Script output:', scriptOutput);
            resolve(scriptOutput);
            if (code != 0) {
                reject(`Script exited with code ${code}`);
            }
        });
    });
};
function run() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const newBranchName = tl.getInput('newBranchName', false) || "";
            const workingDirectory = tl.getInput('workDir', false) || tl.getVariable('Build.SourcesDirectory') || "";
            const pat = tl.getVariable('pat') || tl.getInput('pat', false) || "";
            const openaiUrl = tl.getInput('openaiUrl') || "";
            const openaiModelname = tl.getInput('openaiModelname') || "";
            const openaiKey = tl.getInput('openaiKey') || "";
            const path = require('path');
            const scriptPath = path.join(__dirname, 'python/create-wiki.py');
            console.log("Working directory: " + workingDirectory);
            console.log("Script path: " + scriptPath);
            console.log("OpenAI URL: " + openaiUrl);
            console.log("OpenAI Model name: " + openaiModelname);
            console.log("New Branch Name: " + newBranchName);
            const dep = yield installPythonPackages(path.join(__dirname, 'python/requirements.txt'));
            // Run the python script with input as argument
            const data = yield runScript(scriptPath, [workingDirectory, pat, openaiUrl, openaiModelname, openaiKey, newBranchName, 'false']);
            console.log(data);
        }
        catch (err) {
            tl.setResult(tl.TaskResult.Failed, err.message);
        }
    });
}
run();
