import matplotlib.pyplot as plt
""" fig, ax = plt.subplots()
ax.plot([1,2,3],[10,20,15])
ax.set_title("Example plot ") #simple example for plots
ax.set_xlabel("x_axix")
ax.set_ylabel("y_axix")
plt.show() """

months = ["jan","feb","mar","apr","may"]
website_visits = [4000,5000,2000,2500,3000]
plt.plot(months, website_visits, marker="o",label=" Website Visits")
plt.title("Monthly Website Visits")
plt.xlabel("Months")
plt.ylabel("Website Visits")
plt.grid()
plt.legend()
plt.show()