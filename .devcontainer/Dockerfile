# Dockerfile for developing of tasuren's website.

FROM gcr.io/distroless/nodejs20-debian11

RUN bash -c 'echo -e "\nexport PS1=\"${debian_chroot:+($debian_chroot)}\
\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\
\$ \""' >> ~/.bashrc

# Prepare requirements.
RUN apt-get install -y --no-install-recommends git curl
RUN curl -fsSL https://get.pnpm.io/install.sh | sh -

# Clean.
RUN apt-get clean