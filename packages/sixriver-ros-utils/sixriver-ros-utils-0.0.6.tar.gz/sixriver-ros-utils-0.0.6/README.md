# sixriver_ros_utils

To upload to cloud....
up the version (manual right now)

cd sixriver_ros_utils
rm -rf dist/
python3 setup.py sdist bdist_wheel
python -m twine upload  dist/*