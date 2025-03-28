FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

RUN mkdir /idt_backend
RUN mkdir /idt_backend/runtime
WORKDIR /idt_backend
COPY requirements.txt /idt_backend/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install django-cors-headers

COPY . /idt_backend/runtime
EXPOSE 8000
WORKDIR /idt_backend/runtime

RUN chmod +x /idt_backend/runtime/entrypoint.sh

ENTRYPOINT ["/idt_backend/runtime/entrypoint.sh"]
CMD ["run"]
