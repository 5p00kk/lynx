es_rgb = """
//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04"],
    output: {
      bands: 3,
      sampleType: "AUTO", // default value - scales the output values from [0,1] to [0,255].
    },
  }
}

function evaluatePixel(sample) {
  return [2.5*sample.B04, 2.5*sample.B03, 2.5*sample.B02]
}
"""

es_veg = """
//VERSION=3
function setup() {
  return {
    input: ["B05", "B06", "B07"],
    output: {
      bands: 3,
      sampleType: "AUTO", // default value - scales the output values from [0,1] to [0,255].
    },
  }
}

function evaluatePixel(sample) {
  return [sample.B05, sample.B06, sample.B07]
}
"""

es_rgb_cl = """
//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04", "SCL"],
    output: {
      bands: 3,
      sampleType: "AUTO", // default value - scales the output values from [0,1] to [0,255].
    },
  }
}

function evaluatePixel(sample) {
  if ([8, 9, 10].includes(sample.SCL)) {
    return [1, 0, 0]
  } else {
    return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
  }
}
"""