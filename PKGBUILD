# Maintainer: DaeS
pkgname=impyh
pkgver=20120403
pkgrel=1
pkgdesc="a GUI for scrot written in python"
arch=('i686' 'x86_64')
url="https://github.com/daesdp/Impyh"
license=('GPL')
depends=('python' 'python-gobject' 'scrot')
install=.INSTALL
_gitroot="git://git@github.com/daesdp/Impyh.git"
_gitname="Impyh"

build() {
  msg "Connecting to GIT server...."
  git clone $_gitroot
  cd "${srcdir}/${_gitname}/${pkgname}-${pkgver}"
}

package() {
  msg "Starting to install...."
  cp -Rf "${srcdir}/$_gitname/${pkgname}-${pkgver}"/* "${pkgdir}/"
  chmod 775 ${pkgdir}/usr/share/impyh/ -R
  chmod a+x ${pkgdir}/usr/bin/impyh
}

