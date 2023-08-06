import os
package_dir = os.path.dirname(__file__)
class data:
    NOT_FOUND=open(os.path.join(package_dir,'base.tmp')).read().replace('{title}','404 Page Not Found').replace('{body}',open(os.path.join(package_dir,'404.tmp')).read())
    def ERROR(e):
        return open(os.path.join(package_dir,'base.tmp')).read().replace('{title}','500 Internel Server Error').replace('{body}',open(os.path.join(package_dir,'500.tmp')).read()+str(e))
