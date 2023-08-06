# Copy of test recipe used on drone.io
#
# Configuration:
#    Language:  Python2.7
#    No Database
#    No Environment Variables

# pip -q install .
# pip -q install cram
# cram -v tests/*.t

pip -q install tox
tox

