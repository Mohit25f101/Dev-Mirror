import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {

    // 🔊 Output Channel
    const channel = vscode.window.createOutputChannel("DevMirror");
    channel.show();
    channel.appendLine("🚀 DevMirror Day-2 tracking started");

    // 🧠 STATE
    let currentFile: string | null = null;
    let fileStartTime: number | null = null;
    const timeSpent: Record<string, number> = {};

    let lastEditTime: number | null = null;
    let editCount = 0;

    // 📂 FILE SWITCH TRACK
    const editorSub = vscode.window.onDidChangeActiveTextEditor(editor => {
        const now = Date.now();

        if (currentFile && fileStartTime) {
            const duration = now - fileStartTime;
            timeSpent[currentFile] = (timeSpent[currentFile] || 0) + duration;

            channel.appendLine(
                `⏱ Time spent on ${currentFile}: ${Math.round(timeSpent[currentFile] / 1000)}s`
            );
        }

        if (editor && editor.document) {
            currentFile = editor.document.fileName;
            fileStartTime = now;
            channel.appendLine(`📂 Switched to ${currentFile}`);
        }
    });

    // ✏️ EDIT TRACK
    const editSub = vscode.workspace.onDidChangeTextDocument(event => {
        const now = Date.now();

        if (currentFile && event.document.fileName === currentFile) {
            editCount++;

            if (lastEditTime && now - lastEditTime > 3000) {
                channel.appendLine(`🧠 Edit burst ended — ${editCount} edits`);
                editCount = 0;
            }

            lastEditTime = now;
        }
    });

    // 💾 SAVE TRACK
    const saveSub = vscode.workspace.onDidSaveTextDocument(doc => {
        channel.appendLine(`💾 Saved ${doc.fileName}`);
    });

    // 📊 SUMMARY COMMAND
    const summaryCmd = vscode.commands.registerCommand(
        "devmirror.showSummary",
        () => {
            channel.appendLine("📊 SESSION SUMMARY");

            for (const file in timeSpent) {
                channel.appendLine(
                    `${file} → ${Math.round(timeSpent[file] / 1000)}s`
                );
            }
        }
    );

    // 👋 HELLO COMMAND (OPTIONAL)
    const helloCmd = vscode.commands.registerCommand(
        'Berserkers.helloWorld',
        () => {
            vscode.window.showInformationMessage('Hello World from DevMirror!');
        }
    );

    context.subscriptions.push(
        editorSub,
        editSub,
        saveSub,
        summaryCmd,
        helloCmd
    );
}

export function deactivate() {}
