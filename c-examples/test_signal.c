#include <stdlib.h>

#include <gio/gio.h>
#include <glib.h>
#include <dbus/dbus-glib.h>

#define PROGNAME "test-signal"

static void
signal_handler (GDBusConnection  *connection,
                const gchar      *sender_name,
                const gchar      *object_path,
                const gchar      *interface_name,
                const gchar      *signal_name,
                GVariant         *parameters,
                gpointer         user_data)
{
  GVariant *event = NULL;
  GVariantIter *iter = NULL;
  GVariant *tag = NULL;
  GVariant *value = NULL;

  g_print("\nGot signal: %s\n", signal_name);
  
  if (0 == g_strcmp0(signal_name, "events"))
  {
    g_variant_get(parameters, "(@sa{sv})", &event, &iter);
    g_print("Event type: %s\n", g_variant_get_string(event, NULL));
    while (g_variant_iter_loop(iter, "{@sv}", &tag, &value))
    {
      if (g_variant_is_of_type(value, G_VARIANT_TYPE_STRING))
      {
        g_print("Tag[STRING]: %s = %s\n",
		g_variant_get_string(tag, NULL),
		g_variant_get_string(value, NULL));
      }
      else if (g_variant_is_of_type(value, G_VARIANT_TYPE_INT32))
      {
        g_print("Tag[INT32]: %s = %d\n",
		g_variant_get_string(tag, NULL),
		g_variant_get_int32(value));
      }
      else
      {
        g_print("Tag %s has unexpected type %s\n",
		g_variant_get_string(tag, NULL),
		g_variant_get_type_string(value));
      }
    }
  }

  g_variant_unref(event);
  g_variant_iter_free(iter);
}

int main(int argc, char **argv)
{
  GMainLoop *loop;
  GDBusConnection *connection;
  GError *error;

  loop = g_main_loop_new(NULL, FALSE);
  if (loop == NULL)
  {
    g_assert("Failed to create main loop");
  }

  g_print(PROGNAME ":main Connecting to the D-Bus.\n");
  error = NULL;
  connection = g_bus_get_sync(G_BUS_TYPE_SYSTEM, NULL, &error);
  g_assert_no_error(error);


  g_print(PROGNAME ":main Subscribing signals.\n");
  guint signal_handler_id = g_dbus_connection_signal_subscribe(connection,
                                                               NULL,
							       "com.calix.exos",
							       "events",
							       "/com/calix/exos",
							       NULL,
							       G_DBUS_SIGNAL_FLAGS_NONE,
							       signal_handler,
							       NULL,
							       NULL);
  g_assert_cmpint(signal_handler_id, !=, 0);

  g_main_loop_run(loop);

  g_main_loop_unref(loop);
  g_object_unref(connection);

  return 0;
}

