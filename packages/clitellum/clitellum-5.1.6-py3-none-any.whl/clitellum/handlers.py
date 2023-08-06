from clitellum.services import Context, Publisher


def handler(key):

  def decorator(f):
    HandlerManager.get_instance().add_handler(key, f)
    return f

  return decorator


class HandlerManager:
  """
    Controla los handlers de los mensajes
    """
  _instance = None

  @classmethod
  def get_instance(cls):
    if cls._instance is None:
      cls._instance = HandlerManager()
    return cls._instance

  def __init__(self):
    self.__handlers = dict()

  def add_handler(self, key, class_type):
    self.__handlers[key] = class_type

  def get_handler(self, key):
    """
        Devuelve el putero a la clase del handler que controla el tipo de mensaje
        :param key: Clave de enrutamiento
        :return:
        """
    return self.__handlers[key] if key in self.__handlers else None

  def get_routing_keys(self):
    """
        Devuelve la lista de routing keys de los handlers
        :return: routing key list
        """
    return self.__handlers.keys()

  def clear(self):
    self.__handlers.clear()

  def clone(self):
    handler_manager = HandlerManager()
    for key in self.get_routing_keys():
      value = self.get_handler(key)
      handler_manager.add_handler(key, value)
    return handler_manager


class CiltellumHandler:
  """
    Clase base para los handlers
    """

  def __init__(self):
    self.__message = None
    """
        :rtype: dict
        """
    self.__publisher = None
    """
        :rtype: clitellum.services.Publisher
        """
    self.__context = None
    """
        :rtype: clitellum.services.Context
        """

  def initialize(self, publisher: Publisher, context: Context, message: str):
    """
        Inicializa el handler con los parametros del mensaje amqp
        :param publisher: Publicador
        :param context: Contexto del mensaje
        :param message: Mensaje Amqp
        :return:
        """
    self.__message = message
    self.__publisher = publisher
    self.__context = context

  def _get_message(self):
    """
        Devuelve el mensaje
        :return: Mensaje
        """
    return self.__message

  def _get_header(self, key: str) -> str:
    """
        Devuelve la cabecera asociada a la clave
        :param key: Clave de la cabecera
        :return: Valor de la cabecera
        :rtype: str
        """
    return self.__context.get_item(key)

  def _get_headers(self) -> dict:
    """Devuelve las cabeceras como diccionario

    :return: Cabeceras del mensaje
    :rtype: dict
    """
    return self.__context

  def _has_header(self, key: str) -> bool:
    """Indica si la cabecera existe

    :param key: Clave de la cabecera
    :type key: str
    :return: True si existe, False en caso contrario
    :rtype: bool
    """
    return key in self.__context

  def _add_header(self, key: str, value: str):
    """
        Añade una cabecera o la actualiza
        :param key: Clave de la cabecera
        :param value: Valor de la cabecera
        """
    self.__context.add_header(key, value)

  def handle(self):
    pass

  def _publish(self, message, routing_key: str):
    """
        Publica un mensaje en el broker
        :param message: Mensaje a enviar en string
        :param routing_key: Clave de enrutamiento
        """
    self.__publisher.publish(message, routing_key, self.__context)
