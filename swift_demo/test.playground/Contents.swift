//: Playground - noun: a place where people can play

import UIKit
import Foundation

let a = 1  // 常量定义与初始化，使用类型推断

let b:Int = 1

var c = 1

var d:Int  // 变量声明时，没有初始化要显式给出类型

let meeage = "\(a) and 3 equals to \(a+3)"  // 字符串插入操作

let s = "Swift语言"

s.characters.count

(s as NSString).length


var range = 1..<5  // 1 2 3 4  区间之半闭区间

// var range2 = Range(start:1, end:5)

var range3 = 1...5  // 1 2 3 4 5 区间之全闭区间

let tpl = ("a", "b")  // 元组

var str = "Hello, playground"
