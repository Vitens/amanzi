export default function(path1, path2) {

  var intersections = []

  for(var i = 0; i<path1.length-1; i++) {
    let a0 = path1[i]
    let a1 = path1[i+1]

    let ax1 = a0.x > a1.x ? a1.x : a0.x
    let ax2 = a0.x > a1.x ? a0.x : a1.x
    let ay1 = a0.y > a1.y ? a1.y : a0.y
    let ay2 = a0.y > a1.y ? a0.y : a1.y

    // ignore lines with zero length
    if(a0.x == a1.x && a0.y == a1.y) { continue }

    for(var ii = 0; ii<path2.length-1; ii++) {
      let b0 = path2[ii]
      let b1 = path2[ii+1]
      // ignore lines with zero length
      if(b0.x == b1.x && b0.y == b1.y) { continue }
      // ignore parallel lines which cannot intersect by definition
      if((a0.x == a1.x && b0.x == b1.x) || (a0.y == a1.y && b0.y == b1.y)) { continue }

      let by1 = b0.y > b1.y ? b1.y : b0.y
      let by2 = b0.y > b1.y ? b0.y : b1.y
      let bx1 = b0.x > b1.x ? b1.x : b0.x
      let bx2 = b0.x > b1.x ? b0.x : b1.x

      // if a line vertical
      if(a0.x == a1.x) {
        // ignore touching lines
        if(b0.x == a0.x || b1.x == a1.x) { continue }



        // intersection if b.y between a0.y and a1.y
        if(bx1 < ax1 && bx2 > ax1 && by1 > ay1 && by2 < ay2) {
          intersections.push({x: a0.x, y: b0.y})
        }

      } else {

        // ignore touching lines
        if(b0.y == a0.y || b1.y == a1.y) { continue }

        // ignore 

        if(ax1 < bx1 && ax2 > bx2 && by1 < ay1 && by2 > ay2) {
          intersections.push({x: b0.x, y: a0.y})
        }

      }

    }



  }
  return intersections
}