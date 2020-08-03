# Copyright 1999-2015 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
PYTHON_COMPAT=( python3_7 )

inherit distutils-r1

MY_PN="Flask-Ask"
MY_P="${MY_PN}-${PV}"

DESCRIPTION="Easy Alexa Skills Kit integration for Flask "
HOMEPAGE="https://pypi.org/project/Flask-Ask/"
SRC_URI="mirror://pypi/${MY_PN:0:1}/${MY_PN}/${MY_P}.tar.gz"

LICENSE="BSD"
SLOT="0"
KEYWORDS="~amd64 ~arm64 ~x86"
IUSE="doc examples"

RDEPEND="
	>=dev-python/flask-0.3[${PYTHON_USEDEP}]
	doc? ( dev-python/sphinx[${PYTHON_USEDEP}] )
	dev-python/aniso8601
	<=dev-python/werkzeug-0.16.1
	dev-python/six
	dev-python/pyyaml
	dev-python/pyopenssl"
DEPEND="${RDEPEND}
	dev-python/pyyaml[${PYTHON_USEDEP}]
	dev-python/setuptools[${PYTHON_USEDEP}]"

PATCHES=( "${FILESDIR}"/${P}-setup-r1.patch )

S="${WORKDIR}/${MY_P}"

python_prepare_all() {
	# Prevent un-needed d'loading
	sed -e "s/, 'sphinx.ext.intersphinx'//" -i docs/conf.py || die

	distutils-r1_python_prepare_all
}

python_compile_all() {
	use doc && esetup.py build_sphinx
}

python_install_all() {
	use examples && local EXAMPLES=( example/. )
	use doc && local HTML_DOCS=( docs/_build/html/. )
	distutils-r1_python_install_all
}
