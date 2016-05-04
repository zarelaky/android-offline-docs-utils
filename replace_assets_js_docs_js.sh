DOCROOT=$PWD
MYDIR=$(cd `dirname $BASH_SOURCE`;pwd)
cp -R $MYDIR/scripts $DOCROOT
sed -i "s#http[s]{0,1}://apis.google.com/js/plusone.js#../../scripts/plusone.js#g" $DOCROOT/assets/js/docs.js
