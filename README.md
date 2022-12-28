# MySQL Tables Dict


```
generate mysql data dict
DB_HOST=127.0.0.1
DB_PORT=9037
DB_USER=root
DB_PASS=123456
DATABASE=cosinee
PRODUCT_VERSION=v8

cd $WORKSPACE/contact-center/docs/database

if [ ! -d ./tmp ]; then
    mkdir tmp
fi

set -x
cd tmp
php ../php/generator.php -H$DB_HOST \
    -P$DB_PORT \
    -d$DATABASE \
    -u$DB_USER \
    -p$DB_PASS \
    -v$PRODUCT_VERSION

cd ../docs
pandoc ../tmp/index.html \
    -o index.html \
    -f html \
    --template standalone.html \
    --toc --toc-depth=2

cd ../tmp

if [ -f $DATABASE.dict.zip ]; then
   rm -rf $DATABASE.dict.zip
fi

zip $DATABASE.dict.zip -r ../docs
```