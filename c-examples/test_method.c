#include <stdlib.h>

#include <gio/gio.h>
#include <glib.h>
#include <dbus/dbus-glib.h>

#define PROGNAME "test-method"


int main(int argc, char **argv)
{
  GDBusConnection *connection;
  GVariant *value;
  GVariant *response;
  GError *error;

  g_print(PROGNAME ":main Connecting to the D-Bus.\n");
  error = NULL;
  connection = g_bus_get_sync(G_BUS_TYPE_SYSTEM, NULL, &error);
  g_assert_no_error(error);

  g_print(PROGNAME ":main Invoking method.\n");
  value = g_dbus_connection_call_sync(connection,
                              "com.calix.exos",
                              "/com/calix/exos",
                              "com.calix.exos",
                              "xget",
                              g_variant_new("(s)", "/status/emesh/wifi-metrics-sm"),
                              G_VARIANT_TYPE("(s)"),
                              G_DBUS_CALL_FLAGS_NONE,
                              -1,
                              NULL,
                              &error);
  g_assert_no_error(error);

  g_variant_get(value, "(@s)", &response);
  g_print("Response: %s\n", g_variant_get_string(response, NULL));

  g_variant_unref(value);
                              
  g_object_unref(connection);

  return 0;
}

