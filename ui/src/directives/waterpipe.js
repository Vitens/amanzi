/**
 * Signum, without 0s.
 * @param {number} n The number.
 * @return {number} s -1 for negative, 1 otherwise.
 */
 function sign(n){
	return n < 0 ? -1 : 1;
}

/**
 * Turn -0 into 0.
 * @param {number} n The number.
 * @return {number} n or 0 if n === -0.
 */
function pos0(n){
	return n === -0 ? 0 : n;
}

/**
 * Maximum abs! Returns the greatest of the
 * absolute values.
 * @param {...number} args The numbers.
 * @return {number} max The maximum of the absolutes.
 */
function maxAbs(...args){
	return Math.max.apply(Math, args.map(Math.abs));
}

/**
 * Maps anchor description to x & y directions.
 *
 * @param {string} anc The anchor string, one of
 *                     'left', 'top', 'right' or 'bottom'.
 * @return {Object} dir The direction e.g. `{x: 1, y: 0}`
 *                      for 'right'.
 * @return {number} dir.x Direction on the x-axis: -1, 0 or 1.
 * @return {number} dir.y Direction on the y-axis: -1, 0 or 1.
 */
function anchorDirection(anc){
	if(anc.x && anc.y){
		return anc;
	}

	return {
		'left': {x: -1, y: 0},
		'top': {x: 0, y: -1},
		'right': {x: 1, y: 0},
		'bottom': {x: 0, y: 1}
	}[anc.toLowerCase()];
}

/**
 * @typedef Point
 * @type {Object}
 * @property {number} x The x-coordinate.
 * @property {number} y The y-coordinate.
 * @property {string} anchor The anchor/direction of the
 *                    point. Possible values are: 'top',
 *                    'left', 'bottom' or 'right'.
 */

/**
 * @typedef Dir
 * @type {Object}
 * @property {number} x Direction on the x-axis: -1, 0, or 1.
 * @property {number} y Direction on the y-axis: -1, 0, or 1.
 */

/**
 * The information for `makePath`.
 * @typedef PathInfo
 * @type {Object}
 * @property {Point} start The starting point.
 * @property {Point} end The end point.
 * @property {Point} startStub The start stub point.
 * @property {Point} endStub The end stub point.
 * @property {Dir} startDir The path direction as it
 *               leaves the starting point.
 * @property {Dir} endDir The path direction as it
 *               enters the end point.
 * @property {number} left The left-most point of the bounding box.
 * @property {number} top The top-most point of the bounding box.
 * @property {number} width The width of path bounding box.
 * @property {number} height The height of the path bounding box.
 * @property {boolean} opposite Anchors have opposite directions,
 *                   on the same axis.
 * @property {boolean} facing Anchors have opposite directions,
 *                   but face eachother. OR, if `perpendicular`,
 *                   they are pointing to one common point, or
 *                   facing away from it.
 * @property {boolean} parallel Anchors have same directions, on
 *                   the same axis.
 * @property {boolean} perpendicular Anchors are 90deg apart.
 * @property {boolean} vertical First move from starting point
 *                   is to be on the y axis.
 */

/**
 * Determine the info that `makePath` needs.
 * 
 * @param {Point} start The starting point.
 * @param {Point} end The end point.
 * @param {Object} options Other options.
 * @param {number} options.stubLength The stub-length:
 * 	               the offset between the start/end and
 * 	               the first bend.
 * @return {PathInfo} info The information.
 */
function describe(start, end, options){
	options = options || {};

	options.stubLength = options.stubLength || 0;

	const startDir = anchorDirection(start.anchor),
		endDir = anchorDirection(end.anchor),
		// the real starting point of the path, or more
		// precisely: where the first bend may occur
		startStub = {
			x: start.x + options.stubLength * startDir.x,
			y: start.y + options.stubLength * startDir.y,
			anchor: start.anchor
		},
		// the ending point of the path, or the last possible bend
		endStub = {
			x: end.x + options.stubLength * endDir.x,
			y: end.y + options.stubLength * endDir.y,
			anchor: end.anchor
		},
		// distance between stubs
		dx = endStub.x - startStub.x,
		dy = endStub.y - startStub.y,
		// size of the path bounding box
		width = maxAbs(dx, end.x - start.x, endStub.x - start.x, end.x - startStub.x),
		height = maxAbs(dy, end.y - start.y, endStub.y - start.y, end.y - startStub.y),
		// starting points bounding box
		left = Math.min(start.x, end.x, startStub.x, endStub.x),
		top = Math.min(start.y, end.y, startStub.y, endStub.y),

		ret = {
			start, end,
			startStub, endStub,
			startDir, endDir,
			dx, dy,
			width, height,
			left, top,

			opposite: false,
			facing: false,
			parallel: false,
			perpendicular: false,
			vertical: false
		};

	// start path at the stubs
	start = startStub;
	end = endStub;

	// turn the directions so they 'follow' the path
	// i.e. startDir as the path leaves the starting point
	startDir.x = pos0(startDir.x * sign(dx));
	startDir.y = pos0(startDir.y * sign(dy));
	// ..and endDir as it enters the end point
	endDir.x = pos0(endDir.x * -sign(dx));
	endDir.y = pos0(endDir.y * -sign(dy));

	// this happens to be true for all conditions
	if(startDir.x === -1 || startDir.y === 1){
		ret.vertical = true;
	}

	// Since we only deal with straight lines and angles
	// for both directions, if x is non-zero, then y is 0
	// and vice versa. So if we define 
	// const dir = [startDir.x, startDir.y, endDir.x, endDir.y];
	// Then there are 16 combinations of that array.
	// They are annotated at the conditions.
	
	// [-1,  0, -1,  0]
	// [ 0, -1,  0, -1]
	if((startDir.x === -1 && endDir.x === -1) ||
			(startDir.y === -1 && endDir.y === -1)){
		ret.opposite = true;
	}

	// [ 1,  0,  1,  0]
	// [ 0,  1,  0,  1]
	if((startDir.x === 1 && endDir.x === 1) ||
			(startDir.y === 1 && endDir.y === 1)){
		ret.facing = true;
	}

	// [-1,  0,  1,  0]
	// [ 1,  0, -1,  0]
	// [ 0, -1,  0,  1]
	// [ 0,  1,  0, -1]
	if((startDir.x && startDir.x + endDir.x === 0) ||
			(startDir.y && startDir.y + endDir.y === 0)){
		ret.parallel = true;
	}

	// [-1,  0,  0,  1]
	// [ 1,  0,  0, -1]
	// [ 0, -1,  1,  0]
	// [ 0,  1, -1,  0]
	// (plus the ones below)
	if((startDir.x + endDir.x !== 0) &&
			(startDir.y + endDir.y !== 0)){
		ret.perpendicular = true;

		// [ 1,  0,  0,  1]
		// [-1,  0,  0, -1]
		// [ 0, -1, -1,  0]
		// [ 0,  1,  1,  0]
		if(startDir.x === endDir.y &&
				startDir.y === endDir.x){
			ret.facing = true;
		}else{
			ret.facing = false;
		}
	}

	return ret;
}

/**
 * Make a path.
 *
 * @param {PathInfo} info The information from `describe`.
 * @param {Object} options Other options.
 * @return {Array} path An array of {Point}s (without anchors)
 *                 that describe the path.
 */
function makePath(info, options){
	const dx = info.dx,
		dy = info.dy,
		hx = dx / 2,
		hy = dy / 2,
		ret = [info.start, info.startStub],
		start = info.startStub,
		end = info.endStub;

	// push one point in between: create a right angle
  // if(info.height == 0 || info.width == 0) {
  //   // direct connection, no need for extra enpoints
  // }
	if((info.perpendicular && info.facing) || info.parallel){
		ret.push({
			x: info.vertical ? start.x : start.x + dx,
			y: info.vertical ? start.y + dy : start.y
		});
	// push two points in between: create an s-shape
	}else /* if(info.facing || info.opposite || info.perpendicular)*/ {
		ret.push({
			x: info.vertical ? start.x : start.x + hx,
			y: info.vertical ? start.y + hy : start.y
		}, {
			x: info.vertical ? start.x + dx : start.x + hx,
			y: info.vertical ? start.y + hy : start.y + dy
		});
	}

	ret.push(info.endStub, info.end);
	
	return ret;
}

/**
 * Rotate an anchor (string) clockwise. Only rotates 
 * by 90 degrees. Maps 'left' to 'top' etc. per 90
 * degree increment.
 *
 * @param {string} anchor An anchor ('left', 'top',
 *                 'right' or 'bottom').
 * @param {number} rotation The rotation, in degrees.
 * @return {string} rotated The rotated anchor
 */
function rotate(anchor, rotation){
	rotation = Math.floor(rotation / 90);
	while(rotation--){
		anchor = {
			left: 'top',
			top: 'right',
			right: 'bottom',
			bottom: 'left'
		}[anchor.toLowerCase()];
	}
	return anchor;
}

/**
 * Transform the path into coordinates relative
 * to the bounding box.
 * @param {PathInfo} info The info from `describe`.
 * @param {Array} path The path from `makePath`.
 * @return {Array} rel The path in relative coordinates.
 */
function relativate(info, path){
	const ret = [];
	
	path.reduce((acc, pnt) => {
		const add = {
			x: pnt.x - acc.x,
			y: pnt.y - acc.y
		};
		if(pnt.anchor){
			add.anchor = pnt.anchor;
		}

		ret.push(add);
	}, {x: info.left, y: info.top});

	return ret;
}

export default {
	describe,makePath,rotate,relativate
}