#include <freertos/FreeRTOS.h>
#include "Application.h"
#include <ADCSampler.h>
#include "transports/TCPSocketTransport.h"
#include "config.h"

void Application::begin()
{
  //check max4466 module
  this->input = new ADCSampler(ADC_UNIT_1, ADC1_CHANNEL_0, i2s_adc_config);


  this->input = input;
  this->transport2 = new TCPSocketTransport();
  this->input->start();
  this->transport2->begin();

  //create stream task with highest priority "0"
  TaskHandle_t stream_task_handle;
  xTaskCreate(Application::streamer_task, "stream_task", 8192, this, 0, &stream_task_handle);

  //create text task with lower priority "1"
  TaskHandle_t text_task_handle;
  xTaskCreate(Application::listen_to_text_task, "text_task", 8192, this, 1, &text_task_handle);

}

//for audio stream
void Application::streamer_task(void *param)
{
  Application *app = (Application *)param;
  // now just read from the microphone and send to the clients
  int16_t *samples = (int16_t *)malloc(sizeof(int16_t) * 1024);
  while (true)
  {
    // read from the microphone
    int samples_read = app->input->read(samples, 1024);
    // we use TCP sockets
    app->transport2->send(samples, samples_read * sizeof(int16_t));
  }
}

//for listening to text
void Application::listen_to_text_task(void *param)
{
  Application *app = (Application *)param;
  
  while (true)
  {
    //we use TCP port to listen
    app->transport2->listen_for_text();
  }
}
