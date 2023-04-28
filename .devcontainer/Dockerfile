# Dockerfile for developing of tasuren's website.

FROM node:20-slim

RUN bash -c 'echo -e "\nexport PS1=\"${debian_chroot:+($debian_chroot)}\
\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\
\$ \""' >> ~/.bashrc

# Prepare requirements.
RUN apt-get update && apt-get install -y --no-install-recommends git nano curl ca-certificates
RUN update-ca-certificates
RUN curl -fsSL https://get.pnpm.io/install.sh | bash -

# Clean.
RUN apt-get clean
