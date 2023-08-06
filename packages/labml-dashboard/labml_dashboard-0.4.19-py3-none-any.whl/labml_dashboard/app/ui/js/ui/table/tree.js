define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class RunsTree {
        constructor(allRuns, runs) {
            this.runs = runs;
            this.fullMap = RunsTree.getRunIndexes(allRuns);
            this.treeMap = {};
            this.tree = [];
        }
        static getRunIndexes(runs) {
            let indexes = {};
            for (let runUI of runs) {
                let r = runUI.run;
                indexes[r.uuid] = runUI;
            }
            return indexes;
        }
        getList() {
            this.buildTree();
            let runs = [];
            for (let node of this.tree) {
                runs = runs.concat(this.nodeToList(node));
            }
            return runs;
        }
        getParent(run) {
            let uuid = run.run.load_run;
            if (uuid == null) {
                return null;
            }
            return this.fullMap[uuid];
        }
        addRun(run) {
            let uuid = run.run.uuid;
            if (this.treeMap[uuid] != null) {
                return;
            }
            let parentRun = this.getParent(run);
            let node = { run: run, children: [] };
            if (parentRun == null) {
                run.generations = 0;
                this.tree.push(node);
            }
            else {
                run.generations = parentRun.generations + 1;
                parentRun.children++;
                this.addRun(parentRun);
                this.treeMap[parentRun.run.uuid].children.push(node);
            }
            this.treeMap[uuid] = node;
        }
        buildTree() {
            for (let run of this.runs) {
                this.addRun(run);
            }
        }
        nodeToList(node) {
            let runs = [node.run];
            for (let r of node.children) {
                runs = runs.concat(this.nodeToList(r));
            }
            return runs;
        }
    }
    exports.RunsTree = RunsTree;
});
