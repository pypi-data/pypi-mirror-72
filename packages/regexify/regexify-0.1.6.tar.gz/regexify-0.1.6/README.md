[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div>
  <p>
    <a href="https://github.com/dcronkite/regexify">
      <img src="images/logo.png" alt="Logo">
    </a>
  </p>

  <h3 align="center">regexify</h3>

  <p>
    Utilities/containers for deploying regular expressions.
  </p>
</div>


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



## About the Project 
This package contains a few useful functions and classes for building/using regular expressions.


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python 3.7+

### Installation
 
Install using pip:

`pip install regexify`

## Usage

See the test files for example usage.

### Pattern Trie
Compile multiple terms into a single pattern.

```python
import re
from regexify import PatternTrie

data = ['there', 'hi', 'python', 'pythons', 'hiya']
trie = PatternTrie(*data)
pat = re.compile(trie.pattern)
```

## Versions

Uses [SEMVER](https://semver.org/).

See https://github.com/dcronkite/regexify/releases.

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/dcronkite/regexify/issues) for a list of proposed features (and known issues).


<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. 

See `LICENSE` or https://dcronkite.mit-license.org for more information.



<!-- CONTACT -->
## Contact

Please use the [issue tracker](https://github.com/dcronkite/regexify/issues). 


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/dcronkite/regexify.svg?style=flat-square
[contributors-url]: https://github.com/dcronkite/regexify/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dcronkite/regexify.svg?style=flat-square
[forks-url]: https://github.com/dcronkite/regexify/network/members
[stars-shield]: https://img.shields.io/github/stars/dcronkite/regexify.svg?style=flat-square
[stars-url]: https://github.com/dcronkite/regexify/stargazers
[issues-shield]: https://img.shields.io/github/issues/dcronkite/regexify.svg?style=flat-square
[issues-url]: https://github.com/dcronkite/regexify/issues
[license-shield]: https://img.shields.io/github/license/dcronkite/regexify.svg?style=flat-square
[license-url]: https://kpwhri.mit-license.org/
<!-- [product-screenshot]: images/screenshot.png -->