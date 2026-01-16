import fs from 'fs';
const data = JSON.parse(fs.readFileSync('workflows_utf8.json', 'utf8'));
const workflow = data.data.find(w => w.name.includes("Technical Analysis Engine"));
if (workflow) {
    console.log(`ID: ${workflow.id}`);
    console.log(`Name: ${workflow.name}`);
} else {
    console.log("Workflow not found");
}
