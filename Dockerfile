# Long-term maintained base distribution
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG="C.UTF-8"
ENV LC_ALL="C.UTF-8"
ENV NODE_MAJOR=18 

#Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
		ca-certificates \
        curl \
		git \
        gnupg \
		sudo \ 
        texlive-base \
        texlive-bibtex-extra \
        texlive-fonts-extra \
        texlive-fonts-recommended \
        texlive-plain-generic \
        texlive-latex-extra \
        texlive-publishers

#install nodejs and npm package
RUN sudo mkdir -p /etc/apt/keyrings && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
        echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list && \
        sudo apt-get update && \
        sudo apt-get install nodejs -y

# Add user
RUN useradd -m -G sudo -s /bin/bash kali \
    && echo "kali:kali" | chpasswd \
    && usermod -a -G staff kali

# create a working directory
WORKDIR /home/kali

# Clone the repository
RUN git clone https://github.com/feekosta/JSONSchemaDiscovery 

# set new working directory
WORKDIR /home/kali/JSONSchemaDiscovery

#copy patches. and relevant files
COPY --chown=kali:kali ./karma.patch .
COPY --chown=kali:kali ./package.patch .
COPY --chown=kali:kali ./makefile .
COPY --chown=kali:kali ./smoke.sh .

#run patches
RUN  patch karma.conf.js karma.patch
RUN  patch package.json package.patch

#install global dependencies
RUN npm install -g @angular/cli@13.3.11 && \
    npm install -g typescript@4.6.3

RUN npm install

#clone repo containing the latex code
RUN git clone https://github.com/kalino7/ReproEngReport

#clone datasets for experiment
RUN git clone https://github.com/kalino7/datasets

#make smoke.sh executeable
RUN chmod +x smoke.sh

#Build pdf report
RUN make report

EXPOSE 4200