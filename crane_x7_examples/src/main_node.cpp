#include <ros/ros.h>
#include <string>
#include <std_msgs/Int32.h>
#include <cstdint>
class MainNode
{
public:
    MainNode(ros::NodeHandle &nodeHandle);

    ~MainNode();

    void send(void);

private:
    enum class PROG : int32_t
    {
        start_node1 = 0,
        end_node1,   //1
        start_node2, //2
        end_node2,   //3
        start_node3, //4
        end_node3,   // 5
        start_node4, // 6
        end_node4    //7
    };

    PROG progress;

    void topicCallback(const std_msgs::Int32 &data);

    ros::NodeHandle &nh;

    ros::Subscriber sub;

    ros::Publisher pub;

    std::string Topic_name; // control_progress
};

MainNode::MainNode(ros::NodeHandle &nodehandle) : nh(nodehandle), Topic_name("control_progress")
{
    PROG progress = PROG::start_node1;
    sub = nh.subscribe(Topic_name, 1, &MainNode::topicCallback, this);
    pub = nh.advertise<std_msgs::Int32>(Topic_name, 1);
    ROS_INFO("Successfully launched node.");
}

MainNode::~MainNode(){
    
}
void MainNode::topicCallback(const std_msgs::Int32 &data)
{
    PROG receive = static_cast<PROG>(data.data);
    if (receive == PROG::end_node1)
    {
        progress = PROG::start_node2;
        ROS_INFO("start_node2");
    }
    else if (receive == PROG::end_node2)
    {
        progress = PROG::start_node3;
        ROS_INFO("start_node3");
    }
    else if (receive == PROG::end_node3)
    {
        progress = PROG::start_node4;
        ROS_INFO("start_node4");
    }
    return;
}

void MainNode::send()
{
    std_msgs::Int32 msg;
    msg.data = static_cast<int32_t>(progress);
    pub.publish(msg);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "main_node");
    ros::NodeHandle nodeHandle("~");
    MainNode main_node(nodeHandle);
    ros::Rate r(10);
    while (ros::ok())
    {
        main_node.send();
        ros::spinOnce();
        r.sleep();
    }
    return 0;
}