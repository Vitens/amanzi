import _ from "lodash";
import { defineStore } from "pinia";

export const scenarioStore = (uid) =>
  defineStore("scenario/" + uid, {
    state: () => ({
      name: "Scenario1", // scenario name
      uid: uid,
      models: [],
      connections: [],
      selectedBlocks: [],
      metaData: {
        customMicroComponents: { VOC: [], PFAS: [], Other: [] },
      },
      keyfigureOverwrites: {},
      editingModel: null,
      unsolved: false,
      unsaved: false,
    }),
    actions: {
      selectAll() {
        this.selectedBlocks = this.models.map((m) => m.uid);
      },
      duplicate() {
        this.copy();
        this.paste();
      },
      findAllProductPaths() {
        // Find source nodes (nodes with no incoming products but with outgoing products)
        const sourceNodes = this.models.filter((model) => {
          const hasNoIncoming = !this.connections.some(
            (conn) => conn.type === "product" && conn.tgt === model.uid,
          );
          const hasOutgoing = this.connections.some(
            (conn) => conn.type === "product" && conn.src === model.uid,
          );
          return hasNoIncoming && hasOutgoing;
        });

        // Find sink nodes (no outgoing product connections)
        const sinkNodes = this.models.filter((model) => {
          return !this.connections.some(
            (conn) => conn.type === "product" && conn.src === model.uid,
          );
        });

        const paths = [];

        // Helper function for recursive path finding
        const findPaths = (currentNode, currentPath, visited) => {
          // If we reached a sink node, add the path
          if (sinkNodes.some((node) => node.uid === currentNode)) {
            paths.push([...currentPath]);
            return;
          }

          // Get all outgoing product connections from current node
          const outgoing = this.connections.filter(
            (conn) => conn.type === "product" && conn.src === currentNode,
          );

          // Recursively follow each connection
          // Skip splitters in paths
          for (const conn of outgoing) {
            const targetModel = this.models.find((m) => m.uid === conn.tgt);

            // Normal case for non-splitter nodes
            if (!visited.has(conn.tgt)) {
              visited.add(conn.tgt);
              currentPath.push(targetModel);
              findPaths(conn.tgt, currentPath, visited);
              currentPath.pop();
              visited.delete(conn.tgt);
            }
          }
        };

        // Start path finding from each source node
        for (const sourceNode of sourceNodes) {
          const visited = new Set([sourceNode.uid]);
          // Save the full source model object instead of just the uid
          const sourceModel = this.models.find((m) => m.uid === sourceNode.uid);
          findPaths(sourceNode.uid, [sourceModel], visited);
        }

        return paths;
      },

      copy(cut = false) {
        // copy selected blocks to clipboard

        // if cut, push undo
        if (this.selectedBlocks.length > 0 && cut) {
          this.$pushUndo();
        }

        let clipboard = { models: [], connections: [] };
        for (var uid of this.selectedBlocks) {
          let block = this.models.find((block) => block.uid == uid);
          clipboard.models.push(block);
        }
        for (var conn of this.connections) {
          if (
            this.selectedBlocks.includes(conn.src) &&
            this.selectedBlocks.includes(conn.tgt)
          ) {
            clipboard.connections.push(conn);
          }
        }
        localStorage.setItem("clipboard", JSON.stringify(clipboard));
        // set copyoffset to 10px
        this.copyOffset = 20;
        // if cut, remove selected blocks
        if (cut) {
          this.models = this.models.filter(
            (m) => !this.selectedBlocks.includes(m.uid),
          );
          this.connections = this.connections.filter(
            (c) =>
              !this.selectedBlocks.includes(c.src) &&
              !this.selectedBlocks.includes(c.tgt),
          );
          this.selectedBlocks = [];
        }
      },

      paste() {
        // if no copyoffset (can happen when pasting between scenarios), set to 20px
        if (!this.copyOffset) {
          this.copyOffset = 20;
        }

        // paste from clipboard, offset by 10px, generate new uids
        let clipboard = JSON.parse(localStorage.getItem("clipboard"));
        if (!clipboard) {
          return;
        }
        this.$pushUndo();

        let newModels = [];
        let newConnections = [];
        let uidMap = {};

        for (var model of clipboard.models) {
          let newModel = JSON.parse(JSON.stringify(model));
          // generate new uid
          var newUid = this.generateUID();
          uidMap[model.uid] = newUid;
          // offset position
          newModel.position.x += this.copyOffset;
          newModel.position.y += this.copyOffset;
          // update uid
          newModel.uid = newUid;
          // update name
          newModel.name = this.suggestName(newModel.name);
          // add to new models
          newModels.push(newModel);
          // increment copyoffset
        }
        // update new connections
        for (var conn of clipboard.connections) {
          let newConn = JSON.parse(JSON.stringify(conn));
          newConn.src = uidMap[conn.src];
          newConn.tgt = uidMap[conn.tgt];
          // shift custompath if necessary
          if (newConn.customPath) {
            for (var i = 0; i < newConn.customPath.length; i++) {
              newConn.customPath[i].x += this.copyOffset;
              newConn.customPath[i].y += this.copyOffset;
            }
          }
          newConnections.push(newConn);
        }
        // add new models to scenario
        this.models = this.models.concat(newModels);
        // add new connections to scenario
        this.connections = this.connections.concat(newConnections);
        // select new models
        this.selectedBlocks = newModels.map((m) => m.uid);
        this.copyOffset += 20;
        // set unsolved
        this.unsolved = true;
        this.unsaved = true;
      },

      patchUndo(undo) {
        // update undo state with current model configuration
        undo.models.forEach((m) => {
          if (this.models.find((mdl) => mdl.uid == m.uid)) {
            m.configuration = this.models.find(
              (mdl) => mdl.uid == m.uid,
            ).configuration;
          }
        });
        // unselect all blocks
        this.$patch(undo);
        this.unsolved = true;
        this.unsaved = true;
      },

      // internal
      generateUID() {
        return Math.random().toString(36).substring(2, 8);
      },

      suggestName(name) {
        let names = [];
        for (var m of this.models) {
          names.push(m.name);
        }
        if (!_.includes(names, name)) {
          return name;
        }
        for (var n = 2; n <= 1000; n++) {
          var suggestedName = name.length > 3 ? name + " " + n : name + n;
          if (!_.includes(names, suggestedName)) {
            return suggestedName;
          }
        }
      },

      selectBlock(uid, append = false) {
        // check if uid is already selected
        if (this.selectedBlocks.includes(uid)) {
          return;
        }
        // if append is true, add to selection, otherwise replace selection
        if (!append) {
          this.deselectBlocks();
        }
        this.selectedBlocks.push(uid);
      },

      deselectBlocks() {
        this.selectedBlocks = [];
      },

      deleteSelected() {
        if (this.selectedBlocks.length == 0) {
          return;
        }

        this.$pushUndo();
        for (var uid of this.selectedBlocks) {
          this.deleteBlock(uid, false);
        }
        this.deselectBlocks();
      },
      checkAndUpdateModelParameters(parameters) {
        // filter out duplicate connections
        this.connections = _.uniqBy(
          this.connections,
          (conn) =>
            conn.src + conn.tgt + conn.srcAnchor + conn.tgtAnchor + conn.type,
        );
        // check if all models have all parameters defined in modelspec, else set default value
        for (var m of this.models) {
          for (var param of parameters[m.type]) {
            if (!m.configuration.parameters[param.name]) {
              m.configuration.parameters[param.name] = param.default;
            }
          }
        }
      },

      // block actions
      addModel(modelspecs, defaults, type, name, position, autoConnect) {
        var modelspec = modelspecs[type];
        const model = _.cloneDeep(modelspec.template);
        model.uid = this.generateUID();

        model.name = this.suggestName(name);

        model.type = modelspec.name;
        model.category = modelspec.category;
        model.configuration = model.configuration ? model.configuration : {};

        model.configuration.parameters = {};

        for (var param of defaults) {
          model.configuration.parameters[param.name] = param.default;
        }

        model.position = position;
        // patch function
        this.$pushUndo();

        // autoconnect
        // find closest empty anchor of compatible type and direction for each anchor
        if (autoConnect) {
          for (var anchor of modelspec.canvas.anchors) {
            // find target models that have connections space free
            let target = anchor.direction == "in" ? "out" : "in";
            let closestDistance = Infinity;
            let closestMatch = null;
            let closestModel = null;

            for (var m of this.models) {
              let spec = modelspecs[m.type];
              for (var a of spec.canvas.anchors) {
                // check if anchor is right type and direction
                if (a.type != anchor.type || a.direction != target) {
                  continue;
                }
                // check if anchor is free
                if (
                  (a.direction == "in" &&
                    this.connections.find(
                      (conn) =>
                        conn.tgt == m.uid && conn.tgtAnchor == a.position,
                    )) ||
                  (a.direction == "out" &&
                    this.connections.find(
                      (conn) =>
                        conn.src == m.uid && conn.srcAnchor == a.position,
                    ))
                ) {
                  continue;
                }

                // calculate distance between anchors
                let dx = m.position.x - position.x;
                let dy = m.position.y - position.y;
                let distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < closestDistance) {
                  closestDistance = distance;
                  closestMatch = a;
                  closestModel = m;
                }
              }
            }

            // connect to closest match if found
            if (closestMatch) {
              let src = anchor.direction == "in" ? closestModel.uid : model.uid;
              let tgt = anchor.direction == "in" ? model.uid : closestModel.uid;
              let srcAnchor =
                anchor.direction == "in"
                  ? closestMatch.position
                  : anchor.position;
              let tgtAnchor =
                anchor.direction == "in"
                  ? anchor.position
                  : closestMatch.position;

              this.addConnection(src, tgt, srcAnchor, tgtAnchor, anchor.type);
            }
          }
        }

        this.models.push(model);
        this.unsolved = true;
        this.unsaved = true;
      },
      prepareMove() {
        this.stateBeforeMove = JSON.parse(JSON.stringify(this.$state));
        this.moved = { dx: 0, dy: 0 };
      },

      moveSelection(dx, dy) {
        // invalidate paths for all connections to or from blocks in selections, except for connections between selected blocks
        for (var conn of this.connections) {
          if (
            this.selectedBlocks.includes(conn.src) &&
            !this.selectedBlocks.includes(conn.tgt)
          ) {
            conn.customPath = [];
          } else if (
            !this.selectedBlocks.includes(conn.src) &&
            this.selectedBlocks.includes(conn.tgt)
          ) {
            conn.customPath = [];
          }
        }

        this.moved.dx += dx;
        this.moved.dy += dy;

        // move all selected blocks delta-x and delta-y pixels, invalidate all custom paths for attached connections
        for (var uid of this.selectedBlocks) {
          let block = this.models.find((block) => block.uid == uid);
          block.position.x += dx;
          block.position.y += dy;
          // update custompath for all connections to/from this block
          for (var conn of this.connections.filter(
            (conn) => conn.src == uid || conn.tgt == uid,
          )) {
            for (var i = 0; i < conn.customPath.length; i++) {
              conn.customPath[i].x += dx / 2;
              conn.customPath[i].y += dy / 2;
            }
          }
        }
      },
      commitMove() {
        // if moved, push undo
        if (this.moved.dx != 0 || this.moved.dy != 0) {
          this.$pushUndo(this.stateBeforeMove);
          // set unsaved
          this.unsaved = true;
        }
      },

      deleteBlock(uid, deselect = true) {
        if (deselect) {
          this.$pushUndo();
        }

        // remove block from list of all models
        this.$patch((state) => {
          state.models = state.models.filter((block) => block.uid != uid);
          state.connections = state.connections.filter(
            (conn) => conn.src != uid && conn.tgt != uid,
          );
        });
        if (deselect) {
          this.deselectBlocks();
        }
        this.unsolved = true;
        this.unsaved = true;
      },

      // ===================
      // connections actions
      // ===================
      deselectConnections() {
        // set all connections to deselected
        for (var c of this.connections) {
          c.selected = false;
        }
      },
      selectConnection(index) {
        // deselect all
        this.deselectConnections();

        // draw selected connection on top to prevent overlap of handles
        let con = this.connections.splice(index, 1)[0];
        con.selected = true;
        this.connections.push(con);
      },
      addConnection(src, tgt, srcAnchor, tgtAnchor, type) {
        this.connections.push({
          src: src,
          tgt: tgt,
          srcAnchor: srcAnchor,
          tgtAnchor: tgtAnchor,
          type: type,
          customPath: [],
          customOffset: 0,
          selected: false,
        });
      },
      updateConnectionPath(index, newPath) {
        this.connections[index].customPath = newPath;
      },
      updateConnectionTextOffset(index, newOffset) {
        this.connections[index].customOffset = newOffset;
      },
      deleteConnection() {
        // delete selected connection
        // check if connection is selected
        if (this.connections.filter((conn) => conn.selected).length == 0) {
          return;
        }

        // push undo
        this.$pushUndo();

        for (var i in this.connections) {
          if (this.connections[i].selected) {
            this.connections.splice(i, 1);
            break;
          }
        }

        // set unsolved
        this.unsolved = true;
        this.unsaved = true;
      },

      serialize() {
        var exportObject = {
          name: this.name,
          scenario_version: 1,
          models: this.models,
          connections: this.connections,
          metaData: this.metaData,
          key_figure_overwrites: this.keyfigureOverwrites,
        };

        return exportObject;
      },
      validate() {
        // check and remove any duplicate connections, not sure how this could happen but it does in some cases, might be due to undo/redo operations or copying/pasting operations
        this.connections = _.uniqBy(
          this.connections,
          (conn) =>
            conn.src + conn.tgt + conn.srcAnchor + conn.tgtAnchor + conn.type,
        );

        // check for source and sink nodes
        var source = false;
        var sink = false;

        for (var m of this.models) {
          let spec = this.modelspec[m.type];

          if (spec.source) {
            source = true;
          }
          if (spec.sink) {
            sink = true;
          }
        }

        if (!source && !sink) {
          return {
            valid: false,
            message: "ui.general.messages.missing_source_sink",
          };
        }
        if (!source) {
          return {
            valid: false,
            message: "ui.general.messages.missing_source",
          };
        }
        if (!sink) {
          return { valid: false, message: "ui.general.messages.missing_sink" };
        }

        // check if all connections are made

        for (var m of this.models) {
          let spec = this.modelspec[m.type];

          if (spec.source) {
            source = true;
          }
          if (spec.sink) {
            sink = true;
          }

          // loop over anchors, check if all connections are made
          for (var a of spec.canvas.anchors) {
            if (a.optional) {
              continue;
            } // skip optional anchors
            var connections = [];
            if (a.direction == "in") {
              // check if all incoming connections are made
              connections = this.connections.filter(
                (c) => c.tgt == m.uid && c.tgtAnchor == a.position,
              );
            } else {
              // check if all outgoing connections are made
              connections = this.connections.filter(
                (c) => c.src == m.uid && c.srcAnchor == a.position,
              );
            }
            if (connections.length == 0) {
              return {
                valid: false,
                message: "ui.general.messages.missing_connections",
                data: { name: m.name },
              };
            }
          }
        }

        return { valid: true };
      },
    },
  })();
