<template>
  <svg ref="svg-path-container" class="svg-path-container"></svg>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'


const props = defineProps({
  numberOfRedrawn: Number,
  units: Array,
})

const parentNode = inject('parent')
const links = () => {
  let svgContainer = ref("svg-path-container");
  svgContainer.innerHTML = null;

  drawnLinks(props.units, parentNode, svgContainer);
}

const drawnLinks = (units, node, container) => {
  if (!units || units.length === 0 || !node) {
    return;
  }
  units.forEach((unit) => {
    const unitRef = node.ref(`unit-${unit.id}`)[0];
    const contentDiv = getContentRef(unitRef);
    let svgOuter = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "svg"
    );

    // Link to members block
    if (unitRef.isShowChildren && unit.members && unit.members.length > 0) {
      const membersBlock = unitRef.ref("members");
      const childDiv = membersBlock
        ? membersBlock.ref("content-block")
        : null;
      if (childDiv) {
        let connectingPathInfo = getPathConnectInfo(
          contentDiv,
          childDiv
        );
        let path = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "path"
        );
        path.setAttribute("stroke", PATH_STOKE_COLOR);
        path.setAttribute("stroke-width", PATH_STOKE_WIDTH);
        path.setAttribute("fill", PATH_FILL);
        path.setAttribute("d", connectingPathInfo);
        svgOuter.appendChild(path);
      }
    }

    // Link to sub units
    if (unitRef.isShowChildren && unit.units && unit.units.length > 0) {
      unit.units.forEach((u) => {
        const childRef = unitRef.ref[`unit-${u.id}`][0];
        if (childRef) {
          let childDiv = getContentRef(childRef);
          let connectingPathInfo = getPathConnectInfo(
            contentDiv,
            childDiv
          );
          let path = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "path"
          );
          path.setAttribute("stroke", PATH_STOKE_COLOR);
          path.setAttribute("stroke-width", PATH_STOKE_WIDTH);
          path.setAttribute("fill", PATH_FILL);
          path.setAttribute("d", connectingPathInfo);
          svgOuter.appendChild(path);
          drawnLinks(unit.units, unitRef, container);
        }
      });
    }
    container.appendChild(svgOuter);
  });
}

const getPathConnectInfo = (orgParent, orgChild) => {
  let parentOffsetX = orgParent.offsetLeft + 0.5 * orgParent.offsetWidth;
  let parentOffsetY = orgParent.offsetTop + orgParent.offsetHeight;
  let childOffsetX = orgChild.offsetLeft + 0.5 * orgChild.offsetWidth;
  let childOffsetY = orgChild.offsetTop;

  let svgContainer = ref("svg-path-container");
  svgContainer.setAttribute(
    "width",
    orgParent.offsetWidth +
    (orgParent.offsetLeft > orgChild.offsetLeft
      ? orgParent.offsetLeft
      : orgChild.offsetLeft)
  );
  if (svgContainer.getAttribute("height") < childOffsetY) {
    svgContainer.setAttribute("height", childOffsetY);
  }

  let gapX = childOffsetX - parentOffsetX;
  let gapY = Math.abs(childOffsetY - parentOffsetY);

  let curveX = 0.15 * gapX;
  let curveY = 0.15 * gapY;
  let minCurve =
    orgParent.offsetLeft === orgChild.offsetLeft
      ? Math.abs(curveX)
      : curveY;
  let isClockwise = parentOffsetX > childOffsetX ? 1 : 0;
  let signum = curveX > 0 ? 1 : -1;

  /*
  This path is separated into 3 lines:
  - 1st: vertical line start from parent position Y down and then make a curve
  - 2nd: horizontal line start after 1st line to child position X
  - 3rd: vertical line start after 2nd line to child position
  */
  let endLine1Vertical = parentOffsetY + minCurve;
  let endCurveX = parentOffsetX + minCurve * signum;
  let endCurveY = parentOffsetY + minCurve * 2;
  let endLine2Horizontal = childOffsetX - minCurve * signum;
  let endLine3Vertical = parentOffsetY + minCurve * 3;

  return `M ${parentOffsetX} ${parentOffsetY} V${endLine1Vertical} A${minCurve} ${minCurve} 0 0 ${isClockwise} ${endCurveX} ${endCurveY} H${endLine2Horizontal} A${minCurve} ${minCurve} 0 0 ${1 - isClockwise
    } ${childOffsetX} ${endLine3Vertical} V${childOffsetY}`;
}
const getContentRef = (nodeRef) => {
  return nodeRef.ref("content-block");
}
onMounted(() => {
  links();
})
</script>