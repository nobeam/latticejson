module.exports = {
  title: 'LatticeJSON',
  description: 'A modern lattice file format',
  head: [
    ['link', { rel: "shortcut icon", href: "assets/favicon.ico" }]
  ],
  temp: ".temp",
  ServiceWorker: true,
  base: "/latticejson/",
  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: 'Reference', link: "/reference" },
      { text: 'GitHub', link: "https://github.com/nobeam/latticejson" },
      { text: 'PyPI', link: "https://pypi.org/project/LatticeJSON/" },
      { text: 'Specification', link: "https://github.com/NoBeam/latticejson/blob/master/latticejson/schema.json" }
    ]
  }
};