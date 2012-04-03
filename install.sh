#!/bin/bash

cp -Rf impyh /usr/share
echo "#!/bin/bash" > /usr/bin/impyh
echo "cd /usr/share/impyh && python impyh.py" >> /usr/bin/impyh
chmod 775 /usr/share/impyh/ -R
chmod a+x /usr/bin/impyh

echo "Instalación completa"