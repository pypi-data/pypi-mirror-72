/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#pragma once

#define TC2_ARG(T, prop)                                  \
  auto set_##prop(const T& new_##prop)->decltype(*this) { \
    this->prop##_ = new_##prop;                           \
    return *this;                                         \
  }                                                       \
  auto set_r##prop(T&& new_##prop)->decltype(*this) {     \
    this->prop##_ = std::move(new_##prop);                \
    return *this;                                         \
  }                                                       \
  auto prop(const T& new_##prop)->decltype(*this) {       \
    this->prop##_ = new_##prop;                           \
    return *this;                                         \
  }                                                       \
  auto prop(T&& new_##prop)->decltype(*this) {            \
    this->prop##_ = std::move(new_##prop);                \
    return *this;                                         \
  }                                                       \
  const T& prop() const noexcept {                        \
    return this->prop##_;                                 \
  }                                                       \
  const T& get_##prop() const noexcept {                  \
    return this->prop##_;                                 \
  }                                                       \
  T prop##_
