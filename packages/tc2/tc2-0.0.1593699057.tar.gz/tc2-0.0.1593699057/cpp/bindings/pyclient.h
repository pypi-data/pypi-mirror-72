/*
 * Copyright (c) 2015-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 *
 * This is pretty much equivalent to the main executable, but instead of
 * connecting to a server we'll spin it up ourselves and play against another
 * bot.
 */

#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <torchcraft/client.h>
#include <torchcraft/state.h>

void init_client(pybind11::module& torchcraft) {
  using namespace torchcraft;
  
  pybind11::class_<Client, std::shared_ptr<Client>>(torchcraft, "Client")
    .def(pybind11::init<>())
    .def(
        "connect",
        (bool (Client::*)(const std::string&, int, int)) &Client::connect,
        pybind11::arg("hostname"),
        pybind11::arg("port") = 11111,
        pybind11::arg("timeout") = -1)
    .def(
        "connect",
        (bool (Client::*)(const std::string&, int)) &Client::connect,
        pybind11::arg("file_socket"),
        pybind11::arg("timeout") = -1)
    .def("connected", &Client::connected)
    .def("close", &Client::close)
    .def(
        "init",
        [](Client* self,
           std::pair<int, int> window_size,
           std::pair<int, int> window_pos,
           bool micro_battles) {
          Client::Options opts;
          opts.window_size[0] = window_size.first;
          opts.window_size[1] = window_size.second;
          opts.window_pos[0] = window_pos.first;
          opts.window_pos[1] = window_pos.second;
          opts.micro_battles = micro_battles;

          std::vector<std::string> updates;
          if (self->init(updates, opts)) {
            return pybind11::cast(self->state());
          }
          return pybind11::cast(nullptr);
        },
        pybind11::arg("window_size") = std::make_tuple(-1, -1),
        pybind11::arg("window_pos") = std::make_tuple(-1, -1),
        pybind11::arg("micro_battles") = false,
        pybind11::return_value_policy::reference_internal)
    .def(
        "send",
        [](Client* self, std::vector<std::vector<pybind11::object>> commands) {
          std::vector<Client::Command> to_send;
          for (auto vec : commands) {
            if (vec.size() == 0) {
              continue;
            }

            Client::Command cmd;
            cmd.code = vec[0].cast<int>();
            if (vec.size() > 1) {
              try {
                auto arg1 = vec[1].cast<std::string>();
                cmd.str = arg1;
              } catch (pybind11::cast_error& e) {
                cmd.args.push_back(vec[1].cast<int>());
              }
              for (size_t i = 2; i < vec.size(); i++) {
                cmd.args.push_back(vec[i].cast<int>());
              }
            }
            to_send.push_back(cmd);
          }
          return self->send(to_send);
        })
    .def(
        "recv",
        [](Client* self) {
          std::vector<std::string> updates;
          if (!self->receive(updates)) {
            throw std::runtime_error(
                std::string("Receive failure: ") + self->error());
          }
          return self->state();
        },
        pybind11::return_value_policy::reference_internal)
    .def("poll", &Client::poll)
    .def("error", &Client::error)
    .def("state", &Client::state, pybind11::return_value_policy::reference_internal);
}