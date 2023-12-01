from django.shortcuts import get_object_or_404, render, redirect
from Carts.models import CartItem
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Courses.models import Course, Membership
# Create your views here.


def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_items = CartItem.objects.filter(
        cart_id=request.user.id, is_active=True)

    total_price = 0
    for cart_item in cart_items:
        cart_item.tuition_course = cart_item.courses.tuition_course
        total_price += cart_item.tuition_course
        cart_item.ImageURL = cart_item.courses.ImageURL
        cart_item.name = cart_item.courses.name
        cart_item.duration_course = cart_item.courses.get_duration_display
        cart_item.schedule_course = cart_item.courses.get_schedule_display
        cart_item.time_course = cart_item.courses.time_course

    # Trả về template hiển thị giỏ hàng
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required(login_url='login')
def add_to_cart(request, course_id):  # thêm vào giỏ hàng
    if not request.user.is_authenticated:
        return redirect('login')
    course = get_object_or_404(Course, pk=course_id)
    if course.quantity_member == 0:
        messages.error(request, 'Khóa học đã hết chỗ!')
        return redirect('home')
    # Kiểm tra xem khóa học đã tồn tại trong membership hay không
    if Membership.objects.filter(user=request.user, course=course).exists():
        messages.error(request, 'Bạn đã đăng ký khóa học này rồi!')
        return redirect('home')
    cart_items = CartItem.objects.filter(
        cart_id=request.user.id, is_active=True)
    cart_item = None
    for item in cart_items:
        if item.courses == course:
            cart_item = item
            break
    if cart_item is None:
        cart_item = CartItem.objects.create(
            cart_id=request.user.id, courses=course)
        return redirect('cart')
    else:
        messages.error(request, 'Đã có sản phẩm trong giỏ hàng!')
        return redirect('course_detail', course_id=course_id)


@login_required(login_url='login')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('cart')
